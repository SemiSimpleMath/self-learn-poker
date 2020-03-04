
import torch
import torch.nn as nn
import copy
import ev_state_logic
import math
import models
import numpy

EV_LOST = 0
EV_LOST_1 = 0
EV_LOST_2 = 0


def multi_player_RMSE_loss(output, hand, action_taken_by_model, action_list, opponent_list):
    global EV_LOST
    ev_lists = []
    for opponent in opponent_list:
        ev =  ev_state_logic.get_q_value_list(hand, action_list, opponent)
        ev_lists.append(ev)

    a = numpy.array(ev_lists)

    a = numpy.mean(a, axis=0)

    lost_target = torch.FloatTensor(a)/20

    criterion = torch.nn.MSELoss()

    loss = criterion(output, lost_target)

    ev = a.tolist()

    EV_LOST += ev_state_logic.ev_lost_by_action(ev, action_taken_by_model)

    return loss



def multi_player_RMSE_and_cross_entropy_loss(output, hand, action_taken_by_model, action_list, opponent_list):

    output_1, output_2 = output

    action_taken_by_model_1, action_taken_by_model_2 = action_taken_by_model

    global EV_LOST_1
    global EV_LOST_2
    global EV_LOST

    ev_lists = []
    for opponent in opponent_list:
        ev =  ev_state_logic.get_q_value_list(hand, action_list, opponent)
        ev_lists.append(ev)

    a = numpy.array(ev_lists)

    a = numpy.mean(a, axis=0)

    max_index = numpy.argmax(a)

    lost_target_1 = torch.FloatTensor(a)/20

    criterion1 = torch.nn.MSELoss()

    loss_1 = criterion1(output_1, lost_target_1)

    class_target = [max_index]
    
    target_2 = torch.LongTensor(class_target)

    criterion2 = torch.nn.CrossEntropyLoss()

    loss_2 = criterion2(output_2, target_2)

    ev = a.tolist()

    EV_LOST_1 += ev_state_logic.ev_lost_by_action(ev, action_taken_by_model_1)
    EV_LOST_2 += ev_state_logic.ev_lost_by_action(ev, action_taken_by_model_2)

    loss =  loss_1 + loss_2



    return loss

def RMSELoss(output, hand, action_taken_by_model, action_list, opponent):

    global EV_LOST

    qv =  ev_state_logic.get_q_value_list(hand, action_list, opponent)
 #   sign = lambda x: -1 if x < 0 else (1 if x > 0 else 0)

 #   [sign(x)*math.log(abs(x)) for x in qv]

    lost_target = torch.FloatTensor([qv])/20

    criterion = torch.nn.MSELoss()

    loss = criterion(output, lost_target)



    EV_LOST += ev_state_logic.ev_lost_by_action(qv, action_taken_by_model)

    return loss







def RMSE_and_cross_entropy_loss(output, hand, action_taken_by_model, action_list, opponent):

    output_1, output_2 = output
    action_taken_by_model_1, action_taken_by_model_2 = action_taken_by_model

    global EV_LOST_1
    global EV_LOST_2

    ev =  ev_state_logic.get_q_value_list(hand, action_list, opponent)

    max_index = ev.index(max(ev))

    lost_target_1 = torch.FloatTensor([ev])/20

    criterion1 = torch.nn.MSELoss()

    loss_1 = criterion1(output_1, lost_target_1)

    class_target = [max_index]
    
    target_2 = torch.LongTensor(class_target)

    criterion2 = torch.nn.CrossEntropyLoss()

    loss_2 = criterion2(output_2, target_2)


    EV_LOST_1 += ev_state_logic.ev_lost_by_action(ev, action_taken_by_model_1)
    EV_LOST_2 += ev_state_logic.ev_lost_by_action(ev, action_taken_by_model_2)

    loss =  .1 * loss_1 + loss_2

    return loss









def weights_with_ev_loss(output, hand, action_list):

    qv =  ev_state_logic.get_q_value_list(hand, action_list)
    loss_list = ev_state_logic.get_ev_lost_list(qv)

    lost_list_tensor = torch.FloatTensor([loss_list])
    output = torch.softmax(output,-1)
    output = output * lost_list_tensor

    loss =( (output)**2).sum()

    action_taken = models.action_taken_by_model(output)

    EV_LOST += models.ev_lost_by_action(qv, action_taken)


    return loss

def single_target_distance_loss(output, hand, action_list):

    global EV_LOST

    qv =  ev_state_logic.get_q_value_list(hand, action_list)
    ev_target = max(qv)
    ev_index = qv.index(ev_target)

    loss_list = ev_state_logic.get_ev_lost_list(qv)

    ev_target_list = [0,0,0,0]
    ev_target_list[ev_index] = 1
        
    ev_target_tensor = torch.FloatTensor([ev_target_list])

    output = torch.softmax(output,-1)

    loss = ((ev_target_tensor - output)**2).sum()
 
    action_taken = models.action_taken_by_model(output)

    EV_LOST += models.ev_lost_by_action(qv, action_taken)

        
    return loss





def distance_loss(output, hand, action_list):

    global EV_LOST

    qv =  ev_state_logic.get_q_value_list(hand, action_list)

    loss_list = ev_state_logic.get_ev_lost_list(qv)

    ev_targets = ev_state_logic.get_ev_targets(qv)
        
    ev_targets = torch.FloatTensor([ev_targets])

    output = torch.softmax(output,-1)

    loss = ((ev_targets - output)**2).sum()

    action_taken = models.action_taken_by_model(output)

    EV_LOST += models.ev_lost_by_action(qv, action_taken)
        
    return loss




def multiLoss(output, hand, action_list):

    global EV_LOST

    qv =  ev_state_logic.get_q_value_list(hand, action_list)

    classes =  ev_state_logic.format_q_vector_to_class_vector(qv.copy())

    classes = torch.FloatTensor(classes)
        
#     class_weights = ev_state_logic.format_weight_vector(qv.copy())
        
#     class_weights = torch.FloatTensor(class_weights)
        
    multi_criterion_class = nn.MultiLabelSoftMarginLoss(weight=None, reduce=None)
    multi_loss_class = multi_criterion_class(output, classes)

    
    action_taken = models.action_taken_by_model(output)

    EV_LOST += models.ev_lost_by_action(qv, action_taken)
        
    return multi_loss_class



def playerLoss(output1, output2, hand, action_list):
    global EV_LOST

    qv =  ev_state_logic.get_q_value_list(hand, action_list)

    best_ev = max(qv)

    max_index = qv.index(best_ev)

 
    class_target = [max_index]
    
    class_target_tensor = torch.LongTensor(class_target)

    output_values1, output_indices1 = output1.max(1)

    action_taken_by_model = output_indices1.item()

    loss_list = ev_state_logic.get_ev_lost_list(qv)

    lost = loss_list[action_taken_by_model]

    EV_LOST += lost

    target_ev = torch.FloatTensor([best_ev])

    criterion2 = torch.nn.MSELoss()


    criterion1 = torch.nn.CrossEntropyLoss()
 
    loss =  criterion2(output2,target_ev)/200 +  criterion1(output1, class_target_tensor) 

        
    return loss


def cross_entropy_and_ev(output, hand, action_list, range_dict):

    global EV_LOST

    value_part = output

    value_part = torch.softmax(value_part,-1)


    qv =  ev_state_logic.get_q_value_list(hand, action_list, range_dict)

    max_index = qv.index((max(qv)))

    class_target_tensor = torch.LongTensor([max_index])

    action_taken = models.action_taken_by_model(output)
    lost = models.ev_lost_by_action(qv, action_taken)

    EV_LOST += lost

    lost_target_list = [0,0,0,0]

    lost_target_list[action_taken] = lost

    lost_target_list_tensor = torch.FloatTensor([lost_target_list])

    ev_loss = (lost_target_list_tensor * value_part).sum()

    ev_loss = math.log(ev_loss + 1)

    criterion = torch.nn.CrossEntropyLoss()
 
    cel =  criterion(output, class_target_tensor)

    loss =   (cel + ev_loss)/2

        
    return loss


def cross_entropy(output, hand, action_list, range_dict):

    global EV_LOST


    qv =  ev_state_logic.get_q_value_list(hand, action_list, range_dict)

    max_index = qv.index((max(qv)))

    class_target_tensor = torch.LongTensor([max_index])

    action_taken = models.action_taken_by_model(output)
    lost = models.ev_lost_by_action(qv, action_taken)

    EV_LOST += lost


    criterion = torch.nn.CrossEntropyLoss()
 
    cel =  criterion(output, class_target_tensor)

    loss =   cel

        
    return loss
