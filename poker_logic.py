import numpy
import random

class deck:
    def __init__(self, card_list=None):
        if card_list is None:
            card_list = []
        self.d = card_list.copy()

        for i in range (0,13):
            for j in range (0,4):
                self.d.append((i,j))
    def shuffle(self):
        numpy.random.shuffle(self.d)
    def get_cards(self):
        return self.d.copy()
    def draw_card(self):
        self.shuffle()
        c = self.d.pop()
        return c
    def get_hand(self):
        hand=[]
        card1 = self.draw_card()
        card2 = self.draw_card()
        
        if (card1[0] < card2[0]):
            hand.append(card2)
            hand.append(card1)
        elif card1[0] == card2[0]:
            if card1[1] < card2[1]:
                hand.append(card2)
                hand.append(card1)
            else:
                hand.append(card1)
                hand.append(card2)               
        else:
            hand.append(card1)
            hand.append(card2)
        hand = tuple(hand)
        return hand
    def remove_card(self, hand):
        if hand in self.d:
            self.d.remove(hand)
        else:
            print ("Hand: ", hand)
            print ("not in card_list", self.d)
        return self.d


def get_hand():
    d = deck()
    
    return d.get_hand()


def get_hand_different_from_this_one(hand):

    d = deck()
    hand2 = d.get_hand()
    while hand2[0] == hand[0] or hand2[0] == hand[1] or hand2[1] == hand[0] or hand2[1] == hand[1]:
        hand2 = d.get_hand()
    
    return hand2



class game(deck):
        
    def deal_all_cards(self):
        
        cards = random.sample(self.d, 5)
        return cards
            
    def score_hand(self, hand, cards):
        
        
        total_cards = cards.copy()
        total_cards.extend(hand)
        

        
        
        
        ## Figure out flushes
        found_flush = False
        for i in range (0,3):
            flush_count = 0
            suite = total_cards[i][1]
            max_flush_rank = 0
            for item in total_cards:
                if item[1] == suite:
                    flush_count += 1
                    if item[0] > max_flush_rank:
                        max_flush_rank = item[0]
                    if flush_count >=5:
                        found_flush = True
                
        
        
        ranks = []
        for card in total_cards:
            rank = card[0]
            ranks.append(rank)


        freq_set=set()
        for item1 in ranks:
            count = 0
            for item2 in ranks:
                if item1 == item2:
                    count +=1
            freq_set.add((count,item1))
        
        freq_list=[]
        for item in freq_set:
            freq_list.append(item)
        freq_list.sort()



        ## Figure out straights
        
        ranks.sort()
        straight_count = 0
        straight_high_rank=0
        straight_found = False
        
        for i in range (0,len(ranks)-1):
            if ranks[i]+1 == ranks[i+1]:
                straight_count+=1
                if straight_count >=4:
                    straight_found=True
                    straight_high_rank = ranks[i+1]
            else:
                straight_count = 0
                
        ## TO DO Not checking for straight flushes yet
                
        while len(freq_list) < 5:
            freq_list = [(0,0)] + freq_list

        freq5, freq4, freq3, freq2,freq1 = freq_list[-5:]
                    
        score = 0  
                              
        if freq1[0] == 4:
            score = 70000000000 + freq1[1]
        elif freq1[0] == 3 and freq2[0] == 2:
            score = 60000000000 + 100 * freq1[1] + freq2[1]
        elif found_flush:
            score  = 50000000000 + max_flush_rank # TO DO This is not all there could be mroe to break ties
        elif straight_found:
            score = 40000000000 + straight_high_rank
        elif freq1[0] == 3 and freq2[0] == 1:
            score = 30000000000 + 10000 * freq1[1] + 100 * freq2[1] + freq3[1]
        elif freq1[0] == 2 and freq2[0] == 2:
            score = 20000000000 + 10000 * freq1[1] + 100 * freq2[1] + freq3[1]
        elif freq1[0] == 2 and freq2[0] == 1:
            score = 10000000000 + 1000000 * freq1[1] + 10000 * freq2[1] + 100 * freq3[1] + freq4[1]
        elif freq1[0] == 1:
            score = 100000000 * freq1[1] + 1000000 * freq2[1] + 10000 * freq3[1] + 100 * freq4[1] + freq5[1]
          
            
        # calculate flushes    
        if score == 0:
            a=1
        return score



