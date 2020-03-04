#------Torch------#
import torch
from torch import optim

#------Numpy------#
import numpy

#------Utility------#
import copy

#------My imports------#
import cnfg
import loss_functions
import random
import logs
import models
import hand_functions

class Player:
    def __init__(self, id, Model = models.ModelPlayer, loss_function = loss_functions.RMSELoss):

        ################# MODEL ######################

        self.ModelType = Model
        self.model = Model()
        self.model.train()
        self.optimizer = optim.SGD(self.model.parameters(), lr=0.01, momentum=0.0 )
        self.loss_function = loss_function
        self.use_multiplayer_loss = False
        self.model_name = "PlayerModel"


        ##############PLAYER THINGS #################

        self.id = id
        self.num_hands = 250000
        self.USE_HIGH_LOSS_MITIGATION = False
        self.last_n_to_train_against = "All"
        self.num_to_train_against = "All"
        ###########RANGE DICT ########################
        self.RD = dict()
        self.train_keys = []
        self.RD[()] = cnfg.MCT_PROB_LIST
        self.use_probabilistic_opponent_model = True
        self.trans_prob_data = None
        self.epsilon_prob = 0.00000001

        #############################################


############################################################### PLAYER CODE ###########################################################

    def train(self, opponent_list):

        loss_functions.EV_LOST = 0
        running_loss = 0

        high_loss_states = []

        print ("------------------------ Model", self.id, " training ------------------------")
    
        for i in range (0,self.num_hands):

            if self.last_n_to_train_against != "All" and len(opponent_list) > self.last_n_to_train_against:
                opponent = random.choice(opponent_list[-self.last_n_to_train_against:])
            else:
                opponent = random.choice(opponent_list)
            self.model.parameters_opponent = opponent.model.parameters_self

            self.optimizer.zero_grad()
        
            #if (i > 25000) and random.random() > .9 and len(high_loss_states) > 0:
            #    high_loss_state = high_loss_states[random.randint(0,len(high_loss_states)-1)]
            #    hand, action_list = high_loss_state
            #    high_loss_states.remove(high_loss_state)
            #else:

            hand = hand_functions.get_random_hand_from_list(cnfg.HS_LIST) #cnfg.HAND_LIST[random.randint(0,len(cnfg.HAND_LIST) - 1)] # This line will change
     
            hand = hand_functions.put_hand_in_standard_form(hand)

            action_list = opponent.get_random_key()

            oheh = self.model.encode_hand(hand,action_list)
    
            output = self.model(oheh)
            
            if len(output) == 1:
                action_taken = self.model.deterministic_action_taken_by_model(output)
            else:
                action_taken = self.model.deterministic_double_action_taken_by_model(output)

            if self.use_multiplayer_loss:
                if self.num_to_train_against != "All" and len(opponent_list) >= self.num_to_train_against:
                    opp_list = random.sample(opponent_list,self.num_to_train_against)
                else:
                    opp_list = opponent_list
                loss =  self.loss_function(output, hand,action_taken, action_list, opp_list) #action_list must be common to all opponents data must be prepared for this
            else:
                loss =  self.loss_function(output, hand,action_taken, action_list, opponent)

            #running_loss += loss.item()
 

            #if i > 20000 and loss.item() > 10 * running_loss / i:
            #    high_loss_states.append((hand,action_list))

            loss.backward()

            self.optimizer.step()
        
            output_every = 2000


            if (i % output_every == 0) and i != 0:
                print ("Run number: ", i)
                #print("running loss:", running_loss/ output_every )
                print ("running loss:", running_loss / output_every)
                print ("EV lost: ", loss_functions.EV_LOST/ output_every)
                print ("EV lost 1: ", loss_functions.EV_LOST_1/ output_every)
                print ("EV lost 2: ", loss_functions.EV_LOST_2/ output_every)
                print ("-----------------------------------")
                running_loss = 0
                #if loss_functions.EV_LOST/ output_every < .03:
                #    break
                loss_functions.EV_LOST = 0 
                loss_functions.EV_LOST_1 = 0
                loss_functions.EV_LOST_2 = 0
        self.create_range_dict()       
        self.id += 1

############################################################### MODEL CODE ###########################################################


    def save_model(self, save_file = None):
        if save_file == None:
            id = str(self.id)
            self.model.save_model(self.model_name + id, self.model, self.optimizer)
        else:
            self.model.save_model(self.model_name, self.model, self.optimizer, save_file)
            
    def load_model(self, model_load_file = None):
        id = str(self.id)
        if model_load_file == None:
            self.model = self.model.load_model(self.model_name + id, self.model, self.optimizer, training=True)
        else:
            self.model = self.model.load_model(self.model_name + id, self.model, self.optimizer, True, model_load_file )

        self.create_range_dict()


    def generate_biased_stats(self):
        self.model.generate_biased_stats()
        self.create_range_dict()





############################################################### RANGE CODE ###########################################################





    def create_initial_range_dict(self):

        range_list = []

        range_list.append(cnfg.MCT_PROB_LIST)
        range_list.append(cnfg.MCT_PROB_LIST)

        self.RD = {}

        self.RD[()] = cnfg.MCT_PROB_LIST

        self.generate_initial_range_dict([],range_list)

        self.generate_train_keys()

        self.set_trans_prob_by_street()

        return


    def generate_initial_range_dict(self, action_list, range_list):

        player = len(action_list) % 2

        if len(action_list) == 0:
            possible_actions = [1,2,3]

        if len(action_list) == 1:
            if action_list[-1] == 3:
                possible_actions = [0,1]
            elif action_list[-1] == 2:
                possible_actions = [0,1,2,3]
            elif action_list[-1] == 1:
                possible_actions = [1,2,3]

        if len(action_list) > 1:
            if action_list[-1] == 3:
                possible_actions = [0,1]
   
            elif action_list[-1] == 2:
                possible_actions = [0,1,2,3]
            
        if len(action_list) >= 3:
            if action_list[-3:] == [2,2,2]:
                possible_actions = [0,1,3]       


        for action in possible_actions:
            hands = []
            hands = cnfg.MCT_PROB_LIST
                
            key_list = action_list + [action]
            key_tuple = tuple(key_list)
                
            self.RD[key_tuple] = hands
                
            temp_range_list = range_list.copy()
            temp_range_list[player] = hands
                
            if action != 0 and action !=1:
                self.generate_initial_range_dict(action_list + [action], temp_range_list)

            if action == 1 and len(action_list) == 0:
                self.generate_initial_range_dict(action_list + [action], temp_range_list)
        return


    def create_range_dict(self):

        range_list = []

        range_list.append(cnfg.MCT_PROB_LIST)
        range_list.append(cnfg.MCT_PROB_LIST)

        self.RD = {}

        self.RD[()] = cnfg.MCT_PROB_LIST

        self.generate_range_dict([],range_list) # will use bias if it is set in model

        self.generate_train_keys()
     
        self.set_trans_prob_by_street() # calculates new parameters_self for model


    def generate_range_dict(self, action_list, range_list):
        
        player = len(action_list) % 2

        if len(action_list) == 0:
            possible_actions = [1,2,3]

        if len(action_list) == 1:
            if action_list[-1] == 3:
                possible_actions = [0,1]
            elif action_list[-1] == 2:
                possible_actions = [0,1,2,3]
            elif action_list[-1] == 1:
                possible_actions = [1,2,3]

        if len(action_list) > 1:
            if action_list[-1] == 3:
                possible_actions = [0,1]
   
            elif action_list[-1] == 2:
                possible_actions = [0,1,2,3]
            
        if len(action_list) >= 3:
            if action_list[-3:] == [2,2,2]:
                possible_actions = [0,1,3]       


        for action in possible_actions:
            hands = []

            hands = self.find_sub_range(action_list, action, range_list)
                
            key_list = action_list + [action]
            key_tuple = tuple(key_list)
                
            self.RD[key_tuple] = hands
                
            temp_range_list = range_list.copy()
            temp_range_list[player] = hands
                
            if action != 0 and action !=1 or (action == 1 and len(action_list) == 0):
                self.generate_range_dict(action_list + [action], temp_range_list)

        return


    def find_sub_range(self, action_list, action, range_list):
    

        hands = []

        player = len(action_list) % 2
    
        for item in range_list[player]:
            hand, prob = item
            if self.use_probabilistic_opponent_model:
                action_probability = self.get_propability_list(hand, action_list)
                
                if self.model.use_biased_stats:
                    action_probability = self.model.modify_action_probability_based_on_bias(action_probability)

                action_probability = action_probability[action] * prob 
               
            else:
                max_action_list = self.get_max_action_list(hand, action_list)

                action_probability = max_action_list[action] * prob 

            if action_probability > 0:
                hands += [(hand, action_probability)]
            if action_probability == 0:
                hands += [(hand, self.epsilon_prob)]
        return hands

    def get_max_action_list(self, hand, action_list):
        oheh = self.model.encode_hand(hand, action_list, self.model.parameters_opponent)

        output = self.model(oheh)

        if len(output) == 2:
            output1, output2 = output
            output = output1

        output_values, output_indices = output.max(1)
        action = output_indices.item()

        max_action_list = [0,0,0,0]
        max_action_list[action] = 1

        return max_action_list

    def get_propability_list(self, hand, action_list):
    
        oheh = self.model.encode_hand(hand, action_list)
        action_logits = self.model(oheh)

        if len(action_logits) == 2:
            output1, output2 = action_logits
            action_logits = output1

        ev_list = action_logits.tolist()[0]

        m = max(ev_list)

        if m < 0:
            ev_list[:] = [x/m for x in ev_list]

            ev_list[:] = [1/x for x in ev_list]

        if m > 0:
            for i in range(0, len(ev_list)):
                if ev_list[i] < 0:
                    ev_list[i] = 0
                else:
                    ev_list[i] /= m

        if m == 0:
            for i in range(0, len(ev_list)):
                if ev_list[i] !=m:
                    ev_list[i] = 0
                if ev_list[i] == m:
                    ev_list[i] = 1
    

        prob_list = [x/sum(ev_list) for x in ev_list]

        return prob_list


    def generate_train_keys(self):


        self.train_keys = self.RD.keys()
        self.train_keys = [list(item) for item in self.train_keys]
        self.train_keys = self.make_keys_legal(self.train_keys)

        return
    



    def make_keys_legal(self,keys):

        good_ones=[]

        for key in keys:

            if len(key) > 1:
                if key[-1] != 0 and key[-1] != 1:
                    if self.RD[tuple(key)] != []:
                        good_ones.append(key)

            elif len(key) == 1 and key[-1] !=0 and self.RD[tuple(key)] != []:
                good_ones.append(key)

            elif len(key) == 0:
                good_ones.append([])

        return good_ones


    def get_random_key(self):
        return self.train_keys[random.randint(0,len(self.train_keys)-1)]


    def get_range_from_action_list(self,action_list):

        action_tuple = tuple(action_list)
        try:
                hand_range = self.RD[action_tuple]
        except:
            print ("Action list not found in dict: ", action_list)
 
        return hand_range

    def print_range_dict(self):
        import pprint as pp
        pp.pprint(self.RD)




    def set_trans_prob_by_street(self):

        action_lists = [[],[1],[2],[3],[1,2],[1,3],[2,2],[2,3],[1,2,2],[1,2,3],[2,2,2],[2,2,3],[1,2,2,2],[1,2,2,3],[2,2,2,3],[1,2,2,2,3]] # [[],[1],[2],[3],[2,2],[2,2,3],[2,2,2], [2,2,2,3]]

        trans_prob_by_street=[]
        trans_prob_all_in = []

        for action_list in action_lists:

            trans_prob = [0,0,0,0]
    
            possible_actions=[0,1,2,3]
    
            if len(action_list) > 1:
                if action_list[-1] == 3:
                    possible_actions = [0,1]
                if action_list[-1] == 0 or action_list[-1] == 1:
                    possible_actions = []
        
            if len(action_list) == 1:
                if action_list[-1] == 3:
                    possible_actions = [0,1]
                if action_list[-1] == 0:
                    possible_actions = []
                if action_list[-1] == 1:
                    possible_actions = [1,2,3]   

            if action_list == []:
                possible_actions = [1,2,3]
        
            if len(action_list) >=3:
                if action_list[-3:] == [2,2,2]:
                    possible_actions = [0,1,3]
    
            for i in possible_actions:
                hand_range = self.get_range_from_action_list(action_list + [i])
                count=0
                if len(hand_range) > 0:
                    for item in hand_range:
                        hand_in_range,prob = item
                        count += get_hand_freq(hand_in_range) * prob
                trans_prob[i] = count
        
            total = sum(trans_prob)
            if total !=0:
                trans_prob[:] = [x / total for x in trans_prob]
            else:
                trans_prob = [0,0,0,0]

            trans_prob_by_street.append(trans_prob)



        #all_in_probs = numpy.mean(trans_prob_all_in,0)


        trans_prob_by_street = numpy.concatenate(trans_prob_by_street, 0)

        trans_prob_by_street = numpy.reshape(trans_prob_by_street, (1,64))


        self.model.parameters_self = trans_prob_by_street

        return



    def print_parameters(self):
        action_lists = [[],[1],[2],[3],[1,2],[1,3],[2,2],[2,3],[1,2,2],[1,2,3],[2,2,2],[2,2,3],[1,2,2,2],[1,2,2,3],[2,2,2,3],[1,2,2,2,3]] # [[],[1],[2],[3],[2,2],[2,2,3],[2,2,2], [2,2,2,3]]

        j = 0
        for a in action_lists:
            print(a)
            for i in range(j,j+4):
                print(self.model.parameters_self[0][i])
            j+=4



def get_hand_freq(hand):
    rank1 = hand[0][0]
    rank2 = hand[1][0]

    suite1 = hand[0][1]
    suite2 = hand[1][1]

    if suite1 == suite2:
        count = 4
    if rank1 == rank2:
        count = 6
    if suite1 != suite2  and rank1 != rank2:
        count = 12

    return count


