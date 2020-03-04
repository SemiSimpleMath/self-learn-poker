#-----Torch imports------#
import torch
import torch.nn as nn
from torch.autograd import Variable
import torch.nn.functional as F
from torch import optim

import numpy

import random
import cnfg
import init

import encode_hands
import loss_functions
import ev_state_logic

EV_LOST = 0



class ModelPlayer(nn.Module):
    def __init__(self):

        self.parameters_self = numpy.zeros((1,64))
        self.parameters_opponent = numpy.zeros((1,64))

        self.use_opponent_parameters = False
        self.use_probabilistic_action = True
        self.biased_stats = None

        self.use_biased_stats = False

        super().__init__()
        self.input  = nn.Linear(104,250)
        self.hidden = nn.Linear(250, 100)
        self.output = nn.Linear(100, 4)

  
    def forward(self, x):
        x = self.input(x)
        x = F.leaky_relu(x)
        x = self.hidden(x)
        x = F.leaky_relu(x)
        x = self.output(x)
        return x    



 #This function assumes that the hand is in standard form
    def encode_hand(self, hand, action_list):
    

        rank1 = hand[0][0]
        rank2 = hand[1][0]
        suite1 = hand[0][1]
        suite2 = hand[1][1]

        #first 0-12 are rank hand1
        #next 13-16 are suite hand1
        #next 17-29 are rank2
        #next 30-33 are suite2
        #next is agent A first round index 34
        #next is agent B second round
        #next is agent A third round
        #next is agent B fourth round
        #next is agent A fifth round
        #next is agent B sixth round index 39
        #next are agression transition probabilities for fold, call, raise, rai
        # for 5 streets.  Last 1 is fold to all in %

        zero_tensor = torch.zeros(1, 40)
        zero_tensor[0][rank1] = 1
        zero_tensor[0][13+suite1] = 1
        zero_tensor[0][17+rank2] = 1
        zero_tensor[0][30+suite2] = 1

        
        for i in range (0, len(action_list)):
            zero_tensor[0][34+i] = action_list[i]


        opponent_tensor = torch.zeros(1,64)


        if self.use_opponent_parameters:

            opponent_numpy_ar = self.parameters_opponent 
            opponent_tensor = torch.from_numpy(opponent_numpy_ar).type(torch.FloatTensor)
            opponent_tensor.view(1,64)
        final_tensor = torch.cat((zero_tensor, opponent_tensor), 1)

        return final_tensor




    def save_model(self, model_name, model, optimizer, model_save_file = None):
        if model_save_file == None:
            model_save_path=cnfg.SAVE_PATH
            model_save_file=model_save_path + model_name + '.pth'
        biased_stats = self.biased_stats
        torch.save({
                'model_state_dict': model.state_dict(),
                'optimizer_state_dict': optimizer.state_dict(),
                'biased_stats': self.biased_stats,
                'use_biased_stats': self.use_biased_stats,
                'use_opponent_parameters': self.use_opponent_parameters,
                'parameters_self': self.parameters_self
                }, model_save_file)
        return

    def load_model(self, model_name, model, optimizer, training=True, model_load_file=None):
        if model_load_file == None:
            model_path = "data/training/models/"
            model_load_file = model_path + model_name + '.pth'
        checkpoint = torch.load(model_load_file)
        sd = checkpoint['model_state_dict']
        model.biased_stats = checkpoint['biased_stats']
        model.use_biased_stats = checkpoint['use_biased_stats']
        model.use_opponent_parameters = checkpoint['use_opponent_parameters']
        model.parameters_self = checkpoint['parameters_self']
        model.load_state_dict(sd)
        optimizer.load_state_dict(checkpoint['optimizer_state_dict'])

        if training:
            model.train()
        else:
            model.eval()
        return model



    def generate_biased_stats(self):
        

        self.biased_stats = [0,0,0,0]

        fold_percent = random.uniform(-.2,.2) 
            
        raise_percent = random.uniform(-.2,.2)

        call_percent = random.uniform(-.2,.2)

        rai_percent = random.uniform(-.2,.2)

        self.biased_stats[0] = fold_percent
        self.biased_stats[1] = call_percent
        self.biased_stats[2] = raise_percent
        self.biased_stats[3] = rai_percent

        self.use_biased_stats = True

        return


    def deterministic_action_taken_by_model(self, output):
    
        if len(output) == 1:
            output_values, output_indices = output.max(1)
            action = output_indices.item()
            return action

        else:
            output_1, output_2 = output
            output_values, output_indices = output_2.max(1)
            action = output_indices.item()
            return action

    def deterministic_double_action_taken_by_model(self, output):
   
            output_1, output_2 = output
            output_values, output_indices = output_1.max(1)
            action_1 = output_indices.item()

            output_values, output_indices = output_2.max(1)
            action_2 = output_indices.item()

            return action_1, action_2

    def modify_action_probability_based_on_bias(self, action_probability):

        probs = [0,0,0,0]

        for i in range(0,4):
            if self.biased_stats[i] >=0:
                ap = action_probability[i]
                delta = 1 - ap
                ap += delta * self.biased_stats[i]
            else:
                ap = action_probability[i]
                ap = ap - abs(self.biased_stats[i]) * ap

            probs[i] = ap

        sum_probs = sum(probs)
        probs = [ x / sum_probs for x in probs]

        return probs


    def probabilistic_action_taken_by_model(self, action_logits):

        if len(action_logits) == 2:
            output1, output2 = action_logits
            action_logits = output1

        ev_list = action_logits.tolist()[0]

        m = max(ev_list)

        if m < 0:
            ev_list = [x/m for x in ev_list]

            prob_list = [1/x for x in ev_list]

            probs = [x/sum(prob_list) for x in prob_list]


        if m > 0:
            for i in range(0, len(ev_list)):
                if ev_list[i] < 0:
                    ev_list[i] = 0
                else:
                    ev_list[i] /= m

            probs = [x/sum(ev_list) for x in ev_list]
        if m == 0:
            for i in range(0, len(ev_list)):
                if ev_list[i] !=m:
                    ev_list[i] = 0
                if ev_list[i] == m:
                    ev_list[i] = 1
            probs = [x/sum(ev_list) for x in ev_list]

        if self.use_biased_stats:
            probs = self.modify_action_probability_based_on_bias(probs)

            probs[:] = [x /sum(probs) for x in probs] 

        return (numpy.random.choice([0, 1, 2, 3], 1,  p=probs)[0]).item()


class ModelPlayerValueHeadClassificationHead(ModelPlayer):
    def __init__(self):
        ModelPlayer.__init__(self)
        super().__init__()
        self.input  = nn.Linear(104,250)
        self.hidden1 = nn.Linear(250, 100)
        self.hidden2 = nn.Linear(250,100)
        self.output1 = nn.Linear(100, 4)
        self.output2 = nn.Linear(100, 4)
    def forward(self, inp):

        x = self.input(inp)
        x = F.leaky_relu(x)
        x = self.hidden1(x)
        x = F.leaky_relu(x)
        x = self.output1(x)

        y = self.input(inp)
        y = torch.relu(y)
        y = self.hidden2(y)
        y = torch.relu(y)
        y = self.output2(y)
        return x,y   

