
import random
import init
import cnfg
import poker_logic
import hand_functions
import numpy
import models
import time
import player
import hand_log
import pprint as pp
import ev_state_logic
import loss_functions
import tournament
import gto_model


def output_action_1(action):

    if action == 0:
        action_string = "folds"
    elif action == 1:
        action_string = "calls"
    elif action == 2:
        action_string = "raises"
    elif action == 3:
        action_string = "raises all in"
    print ("Player 1 ", action_string)
    time.sleep(3)



def output_action_2(action):

    if action == 0:
        action_string = "folds"
    elif action == 1:
        action_string = "calls"
    elif action == 2:
        action_string = "raises"
    elif action == 3:
        action_string = "raises all in"
    print ("Player 2 ", action_string)
    time.sleep(3)



def check_that_actions_are_legal(action_list):
    
    handNotBroken = True
    handOver = False
    

    
    if action_list[-1] == 0:
        # hand is over
        handOver= True

    if action_list[-1] == 1 and len(action_list) > 1:
        # hand is over
        handOver= True
    
    if len(action_list) >=2:
        
        if action_list[-2] == 3 and action_list[-1] != 0 and action_list[-1] !=1:
            # hand broken
            handNotBroken = False
    if len(action_list) > 2:
        if action_list[-2] == 1 and action_list[-1] == 1:
            # hand broken
            handNotBroken = False

    if len(action_list) >=4 and action_list[-4:] == [2,2,2,2]:
        handNotBroken = False
        
    return handOver, handNotBroken
        



def calculate_outcome(action_list, small_blind, player_1_hand, player_2_hand):
    
    
    Moneys=[0,0]

    final_action = action_list[-1]
    
    #First player to act here refers to player #0 it is internal to computation of pots
    #and has nothing to do with player numbers.  Player 0 is simply first person to act

    final_player_to_act = (len(action_list) + 1) % 2
    other_player = (len(action_list)) % 2

    pots, amounts, money_put_in  = ev_state_logic.calculate_pot_from_action_list(action_list)

    if final_action == 0:
        Moneys[final_player_to_act] = -money_put_in[final_player_to_act]
        Moneys[other_player] = pots[-1] - money_put_in[other_player]

        if small_blind == 0:
            return Moneys[0], Moneys[1]
        else:
            return Moneys[1], Moneys[0]


    
    player_1_hand, player_2_hand = hand_functions.prepare_pair (player_1_hand,player_2_hand)
    wrt,hvhties, junk = cnfg.MCT[(player_1_hand, player_2_hand)] #SF_VS_SF[(player_1_hand, player_2_hand)]
    
    player_1_wrt = wrt
    player_2_wrt = 1 - player_1_wrt - hvhties
    
    
    player_1_lrt = 1 - player_1_wrt - hvhties
    player_2_lrt = 1 - player_2_wrt - hvhties
    
    pot_at_end = pots[-1]
    if small_blind == 0:
        money_put_in_player_1 = money_put_in[0] 
        money_put_in_player_2 = money_put_in[1]
    else:
        money_put_in_player_1 = money_put_in[1] 
        money_put_in_player_2 = money_put_in[0]

    pot_to_win_player_1 = pot_at_end - money_put_in_player_1
    pot_to_win_player_2 = pot_at_end - money_put_in_player_2
    
    player_1_money = player_1_wrt * pot_to_win_player_1 - player_1_lrt * money_put_in_player_1
    player_2_money = player_2_wrt * pot_to_win_player_2 - player_2_lrt * money_put_in_player_2

    return player_1_money, player_2_money
    
    
def get_hands():
     hand1 = hand_functions.get_random_hand_from_list(cnfg.HS_LIST)
     hand2 = hand_functions.get_random_hand_from_list(cnfg.HS_LIST)

     while not hand_functions.is_compatible(hand1,hand2):
             hand2 = hand_functions.get_random_hand_from_list(cnfg.HS_LIST)

     return (hand1, hand2)


def lets_play(P1, P2):

    if P2 == "GTO":
        is_gto = True
    else:
        is_gto = False
    player_1_money = 0
    player_2_money = 0


    for i in range (0, cnfg.NUMBER_OF_ROUNDS):
        if cnfg.DEMO:
            print ("Hand #:", i)
    
        player_1_hand, player_2_hand = get_hands()

        small_blind = i % 2

        if cnfg.DEMO:
            print ("Small blind is Player ", i % 2 + 1)
            print("\n")
            print ("Player 1 has: ", player_1_hand)
            print ("Player 2 has: ", player_2_hand)
            print("\n")
            time.sleep(3)

        complete = False
        legal = True
    
        action_list = []
    

        while (not complete) and legal:

            player_1_turn = (len(action_list) + small_blind) % 2 == 0

            if player_1_turn:
                oheh = P1.model.encode_hand(player_1_hand,action_list)
                output = P1.model(oheh)
                if P1.model.use_probabilistic_action:
                    action = P1.model.probabilistic_action_taken_by_model(output)
                else:
                    action = P1.model.deterministic_action_taken_by_model(output)
                if cnfg.DEMO:
                    output_action_1(action)

            else:
                if not is_gto:
                    oheh = P2.model.encode_hand(player_2_hand,action_list)
                    output = P2.model(oheh)
                    if P2.model.use_probabilistic_action:
                        action = P2.model.probabilistic_action_taken_by_model(output)
                    else:
                        action = P2.model.deterministic_action_taken_by_model(output)

                else:
                    action = gto_model.get_gto_action(action_list, player_2_hand)
                if cnfg.DEMO:
                    output_action_2(action)
            action_list += [action]



            complete, legal = check_that_actions_are_legal(action_list)


            if not legal:
                #print("illegal action", action_list)
                break

    
        #--------------------- Resolve the hand ----------------------------
    
            if complete and legal:

                player_1_outcome, player_2_outcome = calculate_outcome(action_list,small_blind, player_1_hand, player_2_hand)

                player_1_money += player_1_outcome
                player_2_money += player_2_outcome

                hand_log.log_hand_and_action(player_1_hand, small_blind, action_list, player_1_outcome)

                if cnfg.DEMO:
                    print ("\nPlayer 1 gets: ", player_1_outcome)
                    print ("Player 2 gets: ", player_2_outcome)
                    print ("\n")
                    print ("Player 1 money: ", player_1_money, "Player 2 money: " , player_2_money)
                    print("")
                    time.sleep(5)
 
        if i % 1000 == 0:
            print ("Run number: ", i)

    print ("Player 1 money: ", player_1_money, "Player 2 money: " , player_2_money)

    return player_1_money, player_2_money



def run_play_session():
    cnfg.DEMO = False
    cnfg.NUMBER_OF_ROUNDS = 2000000

    path = "data/dicts/"
    file = "CFR_optimal_dict_3.p"
    cnfg.GTO_DICT = gto_model.load_optimal_dict(path, file)

    gto_model.create_gto_range_dict(cnfg.GTO_DICT)

    import pprint as pp

    pp.pprint(cnfg.GTO_DICT)

#    tournament.begin_tournament()

    M = models.ModelPlayerValueHeadClassificationHead

    P1 = player.Player(1, M, loss_functions.RMSE_and_cross_entropy_loss)
 
    P1.load_model(cnfg.MODELS_PATH + "save_models/against_gto_no_sf_test.pth")
    P1.model.use_probabilistic_action = True
    #P2.load_model(cnfg.MODELS_PATH + "advanced_models/P_1_13.pth")

    #P1.model.use_probabilistic_action = False

    #P2 = player.Player(2, M, loss_functions.RMSE_and_cross_entropy_loss)
 
    #P2.load_model(cnfg.MODELS_PATH + "advanced_models/P_1_11.pth")

    #P2.model.use_probabilistic_action = False
    P2 = "GTO"
    lets_play(P1,P2)


    #P3.load_model(cnfg.MODELS_PATH + "intermediate_models_2/winners_round_2/P_1_19.pth")

    ##P1.generate_biased_stats()
    ##P3.generate_biased_stats()

    #P1.model.use_opponent_parameters = False
    #P2.model.use_opponent_parameters = False
    ##P3.model.use_opponent_parameters = True

    #P1.model.parameters_opponent = P2.model.parameters_self
    #P2.model.parameters_opponent = P1.model.parameters_self
    #P3.model.parameters_opponent = P2.model.parameters_self


    #print (P1.model.parameters_self)

 
    #P3.model.parameters_opponent = P2.model.parameters_self
    #P2.model.parameters_opponent = P3.model.parameters_self



    #P2.model.use_biased_stats = True
    ##P2.model.generate_biased_stats()
    #print ("Player 1 parameters:")
    #P1.print_parameters()

    #print ("----------------------------------------------------------------------------------")

    #print ("Player 2 parameters:")
    #P2.print_parameters()

    return