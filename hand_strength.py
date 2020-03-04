import cnfg
import hand_functions
import poker_logic

def hand_vs_hand_monte_carlo(hand1,hand2):
    g = poker_logic.game()
    

    g.remove_card(hand1[0])
    g.remove_card(hand1[1])
    
    g.remove_card(hand2[0])
    g.remove_card(hand2[1])
        
    hand1_score = 0
    hand2_score = 0
    ties = 0
        
    for i in range (0,10000):

        deal_cards = g.deal_all_cards()
        
        
        score1 = g.score_hand(hand1, deal_cards)
        score2 = g.score_hand(hand2, deal_cards)
        
        if score1 > score2:
            hand1_score +=1
        if score2 > score1:
            hand2_score +=1
            
        if score1 == score2:
            ties+=1

    total = hand1_score + hand2_score + ties
    
    
    return (hand1_score/total, ties/total)

    


def generate_monte_carlo_table(hand_set):
    #cycle over all cards
    
    hand_vs_hand_dict = {}
    
    progress_counter = 0
    
    for pair in hand_set:

        
        progress_counter +=1
        
        hand1_tuple = pair[0]
        hand2_tuple = pair[1]
        
        hand1_tuple, hand2_tuple = hand_functions.prepare_pair (hand1_tuple,hand2_tuple)

         

        if (hand1_tuple,hand2_tuple) not in hand_vs_hand_dict:
            
            
            wrt = hand_vs_hand_monte_carlo(hand1_tuple,hand2_tuple)

            wins, ties = wrt
            
            count = 1
            
            hand_vs_hand_dict[(hand1_tuple,hand2_tuple)] = (wins,ties,count)
            
        else:
            value = hand_vs_hand_dict[(hand1_tuple,hand2_tuple)]
            wins, ties, count = value
            
            count +=1
            
            hand_vs_hand_dict[(hand1_tuple,hand2_tuple)] = (wins,ties,count)
            
            
        if progress_counter % 5000 == 0:
            print (progress_counter)




    return hand_vs_hand_dict
    
class table_analysis:
    
    def __init__(self, table):
        self.t = table
        
    def lookup_card(self, find_this):
        l = []   
        
        for key in self.t:
            if find_this in key[0]:
                l.append( (key, self.t[key]) )
        return l
    
    def lookup_hand(self, find_this):
                
        l = []   
        
        for key in self.t:
            if find_this == key[0]:
                l.append((key, self.t[key]))
        return l
    
    def look_up_hand_vs_hand(self, hand1, hand2):
        # hand1 and hand2 assumed to have been prepared to be compatible 
        key = (hand1,hand2)
        return self.t[key]
    
    def average_hand_strength(self, hand):
        l = self.lookup_hand(hand)
        total_wins = 0
        total_ties = 0
        total_count = 0
        for matchup , result in l:
            weight = result[2]
            total_wins += weight * result[0]
            total_ties += weight * result[1]
            total_count += weight
        return  ( total_wins / total_count , total_ties/total_count )


def hand_vs_range(hand1, range_list):
    total_wrt=0
    total_ties = 0
    total_count = 0
  
    
    for item in range_list:  
        hand2, prob = item
        hand1, hand2 = hand_functions.prepare_pair (hand1,hand2)

        if not hand_functions.is_compatible(hand1,hand2):
            continue

        wrt, ties, weight = cnfg.MCT[(hand1, hand2)]      #SF_VS_SF[(hand1, hand2)]
        total_wrt   += weight * prob * wrt
        total_ties  += weight * prob * ties
        total_count += weight * prob
        

    if total_count == 0:
        print ("Unknown range: ", hand1, range_list)
    return total_wrt / total_count, total_ties / total_count
            
    
