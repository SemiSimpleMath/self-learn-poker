import cnfg
import models
import dict_utilities
import hand_strength
import hand_functions
import random


def init():
    cnfg.MCT = dict_utilities.load_mct_dict() # MCT is the Monte Carlo hand vs hand strength dictionary
    cnfg.TA = hand_strength.table_analysis(cnfg.MCT)
    cnfg.HS = hand_functions.generate_two_card_hands()
    cnfg.HS_LIST = list(cnfg.HS)
    #cnfg.SF_PROB_LIST = hand_strength.prepare_sf_prob_list(cnfg.SF_LIST)
    #hand_strength.generate_sf_hand_vs_sf_hand_table()
 

def first_time_init():

    cnfg.HS = hand_functions.generate_two_card_hands() # HS is all possible two card hands
    cnfg.FS = hand_functions.generate_hand_pairs() # FS is set of all possible hand vs hand (2 cards vs 2 cards)
    cnfg.SF_LIST = hand_functions.generate_sf_list(cnfg.HS) # SF_LIST is a list of cards in standard form.  This is very compact list of possible one player hands it only contains info about hand rank and if it is suited or not

    cnfg.MCT = hand_strength.generate_monte_carlo_table(cnfg.FS) # This line takes a looooong time to run (hours)
    dict_utilities.save_mct_dict(cnfg.MCT)  
    N = 5
    print (dict(random.sample(cnfg.MCT.items(), N)))
    cnfg.TA = hand_strength.table_analysis(cnfg.MCT)
    cnfg.SF_PROB_LIST = hand_strength.prepare_sf_prob_list(cnfg.SF_LIST)
    hand_strength.generate_sf_hand_vs_sf_hand_table()


        


