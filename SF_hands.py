### SF VS SF HAND STRENGTH

def generate_sf_hand_vs_sf_hand_table():
    for hand1 in cnfg.SF_LIST:
        for hand2 in cnfg.SF_LIST:
            total_wrt = 0
            total_ties = 0
            count = 0
            expanded_sf_list = generate_expanded_sf_list(hand2, hand1)
            weight = len(expanded_sf_list)
            for h2 in expanded_sf_list:
                hand1, h2 = hand_functions.prepare_pair (hand1, h2)
                wrt, ties, c = cnfg.TA.look_up_hand_vs_hand(hand1, h2)
                total_wrt +=wrt
                total_ties +=ties
                count +=1
            cnfg.SF_VS_SF[(hand1,hand2)] = (total_wrt/count,total_ties/count, weight)


def prepare_sf_prob_list(sf_list):
    sf_prob_list=[]
    for item in sf_list:
        sf_prob_list.append((item,1))
    return sf_prob_list


    def create_initial_range_dict(self):

        range_list = []

        range_list.append(cnfg.SF_PROB_LIST)
        range_list.append(cnfg.SF_PROB_LIST)

        self.RD = {}

        self.RD[()] = cnfg.SF_PROB_LIST

        self.generate_initial_range_dict([],range_list)

        self.generate_train_keys()

        self.set_trans_prob_by_street()

        return


    SF_VS_SF = dict()

    SF_LIST = [((11, 0), (2, 0)), ((6, 1), (3, 0)), ((10, 1), (9, 0)), ((6, 1), (2, 0)), ((12, 1), (3, 0)), ((12, 0), (1, 0)), ((5, 0), (2, 0)), ((10, 1), (1, 0)), ((8, 1), (4, 0)), ((10, 0), (1, 0)), ((7, 0), (1, 0)), ((7, 0), (5, 0)), ((11, 1), (5, 0)), ((8, 1), (2, 0)), ((5, 1), (3, 0)), ((6, 1), (4, 0)), ((3, 0), (0, 0)), ((2, 1), (2, 0)), ((11, 0), (4, 0)), ((10, 0), (4, 0)), ((6, 0), (0, 0)), ((11, 0), (9, 0)), ((9, 0), (0, 0)), ((12, 1), (0, 0)), ((6, 1), (0, 0)), ((8, 1), (1, 0)), ((11, 1), (11, 0)), ((11, 1), (7, 0)), ((7, 0), (6, 0)), ((11, 0), (1, 0)), ((7, 1), (2, 0)), ((10, 1), (4, 0)), ((10, 0), (2, 0)), ((7, 0), (3, 0)), ((9, 1), (2, 0)), ((8, 1), (8, 0)), ((6, 1), (6, 0)), ((4, 0), (2, 0)), ((3, 1), (1, 0)), ((12, 1), (5, 0)), ((12, 0), (8, 0)), ((10, 0), (5, 0)), ((9, 0), (7, 0)), ((11, 0), (8, 0)), ((9, 1), (4, 0)), ((9, 0), (8, 0)), ((8, 1), (3, 0)), ((7, 1), (4, 0)), ((11, 1), (0, 0)), ((7, 0), (0, 0)), ((12, 1), (4, 0)), ((5, 1), (5, 0)), ((12, 0), (9, 0)), ((9, 1), (0, 0)), ((5, 0), (0, 0)), ((11, 0), (0, 0)), ((11, 0), (3, 0)), ((8, 0), (0, 0)), ((4, 1), (0, 0)), ((4, 1), (3, 0)), ((2, 0), (0, 0)), ((11, 1), (10, 0)), ((2, 1), (0, 0)), ((3, 0), (2, 0)), ((10, 0), (3, 0)), ((10, 1), (0, 0)), ((8, 1), (0, 0)), ((9, 1), (6, 0)), ((7, 1), (7, 0)), ((10, 0), (6, 0)), ((11, 1), (9, 0)), ((6, 0), (3, 0)), ((9, 1), (9, 0)), ((9, 0), (2, 0)), ((4, 1), (4, 0)), ((3, 1), (2, 0)), ((4, 1), (2, 0)), ((10, 0), (8, 0)), ((9, 0), (4, 0)), ((11, 1), (1, 0)), ((7, 0), (4, 0)), ((11, 1), (4, 0)), ((7, 1), (0, 0)), ((5, 1), (2, 0)), ((10, 1), (6, 0)), ((12, 0), (6, 0)), ((6, 0), (1, 0)), ((12, 1), (11, 0)), ((12, 0), (10, 0)), ((5, 0), (3, 0)), ((1, 1), (0, 0)), ((10, 1), (8, 0)), ((4, 0), (0, 0)), ((11, 1), (3, 0)), ((12, 0), (0, 0)), ((4, 0), (3, 0)), ((10, 0), (7, 0)), ((11, 0), (7, 0)), ((9, 0), (3, 0)), ((1, 0), (0, 0)), ((7, 0), (2, 0)), ((12, 0), (7, 0)), ((6, 0), (2, 0)), ((12, 1), (10, 0)), ((12, 0), (11, 0)), ((12, 0), (4, 0)), ((11, 1), (6, 0)), ((10, 0), (9, 0)), ((0, 1), (0, 0)), ((7, 1), (3, 0)), ((8, 1), (7, 0)), ((8, 0), (2, 0)), ((10, 1), (5, 0)), ((9, 1), (1, 0)), ((12, 0), (5, 0)), ((8, 1), (6, 0)), ((8, 0), (3, 0)), ((10, 1), (2, 0)), ((7, 1), (5, 0)), ((11, 0), (6, 0)), ((9, 0), (1, 0)), ((8, 0), (6, 0)), ((5, 1), (4, 0)), ((11, 1), (2, 0)), ((12, 1), (2, 0)), ((3, 1), (0, 0)), ((8, 0), (1, 0)), ((9, 0), (6, 0)), ((9, 1), (5, 0)), ((2, 0), (1, 0)), ((5, 1), (0, 0)), ((1, 1), (1, 0)), ((3, 0), (1, 0)), ((9, 1), (3, 0)), ((12, 1), (12, 0)), ((8, 0), (7, 0)), ((8, 0), (4, 0)), ((12, 1), (1, 0)), ((10, 1), (3, 0)), ((6, 1), (1, 0)), ((12, 0), (2, 0)), ((12, 1), (9, 0)), ((6, 0), (4, 0)), ((5, 0), (4, 0)), ((10, 0), (0, 0)), ((11, 1), (8, 0)), ((10, 1), (10, 0)), ((9, 1), (8, 0)), ((3, 1), (3, 0)), ((12, 1), (7, 0)), ((4, 0), (1, 0)), ((8, 0), (5, 0)), ((11, 0), (5, 0)), ((2, 1), (1, 0)), ((9, 0), (5, 0)), ((11, 0), (10, 0)), ((12, 0), (3, 0)), ((12, 1), (8, 0)), ((6, 0), (5, 0)), ((9, 1), (7, 0)), ((7, 1), (1, 0)), ((8, 1), (5, 0)), ((5, 0), (1, 0)), ((7, 1), (6, 0)), ((5, 1), (1, 0)), ((12, 1), (6, 0)), ((10, 1), (7, 0)), ((4, 1), (1, 0)), ((6, 1), (5, 0))]
SF_PROB_LIST=[]

    def create_initial_range_dict(self):

        range_list = []

        range_list.append(cnfg.SF_PROB_LIST)
        range_list.append(cnfg.SF_PROB_LIST)

        self.RD = {}

        self.RD[()] = cnfg.SF_PROB_LIST

        self.generate_initial_range_dict([],range_list)

        self.generate_train_keys()

        self.set_trans_prob_by_street()

        return



    


def generate_expanded_sf_list(hand, hand2):
    
    card11 = hand[0]
    card12 = hand[1]
    
    card21 = hand2[0]
    card22 = hand2[1]
    
    rank1 = card11[0]
    rank2 = card12[0]
    
    suite1 = card11[1]
    suite2 = card12[1]
    
    c_list = []
    
    if suite1 != suite2 and rank1 != rank2:
        for i in range(3,-1,-1):
            for j in range (3, -1, -1):
                if i !=j:
                    c1=(rank1,i)
                    c2 = (rank2,j)
                    
                    if c1 !=card21 and c1 != card22 and c2 != card21 and c2!=card22:
                        c_list.append((c1,c2))
                        
                        
    if suite1 == suite2:
        for i in range (3,-1,-1):
            c1=(rank1,i)
            c2 = (rank2,i)
                    
            if c1 !=card21 and c1 != card22 and c2 != card21 and c2!=card22:
                c_list.append((c1,c2))
      
    if rank1 == rank2:
        
        for j in range (3,-1,-1):

            for i in range (j-1,-1,-1):
                c1 = (rank1, j)
                c2 = (rank1, i)

                h = (c1,c2)

                if c1 !=card21 and c1 != card22 and c2 != card21 and c2!=card22:
                    c_list.append(h)

            
        
        
        
    return c_list
 

### SF VS SF HAND STRENGTH

def generate_sf_hand_vs_sf_hand_table():
    for hand1 in cnfg.SF_LIST:
        for hand2 in cnfg.SF_LIST:
            total_wrt = 0
            total_ties = 0
            count = 0
            expanded_sf_list = generate_expanded_sf_list(hand2, hand1)
            weight = len(expanded_sf_list)
            for h2 in expanded_sf_list:
                hand1, h2 = hand_functions.prepare_pair (hand1, h2)
                wrt, ties, c = cnfg.TA.look_up_hand_vs_hand(hand1, h2)
                total_wrt +=wrt
                total_ties +=ties
                count +=1
            cnfg.SF_VS_SF[(hand1,hand2)] = (total_wrt/count,total_ties/count, weight)


def prepare_sf_prob_list(sf_list):
    sf_prob_list=[]
    for item in sf_list:
        sf_prob_list.append((item,1))
    return sf_prob_list



def SF_hand_freq(hand, hand_in_range):

    wrt, dict_items, count = cnfg.SF_VS_SF[(hand,hand_in_range)]

    return count


def generate_sf_list(hs):
    sf_set = set()
    for hand in hs:
        hand = put_hand_in_standard_form(hand)
        sf_set.add(hand)
    sf_list = list(sf_set)
    return sf_list
    

def get_sf_hand():
    random_hand = random.randint(0, len(cnfg.SF_LIST)-1)
    hand = cnfg.SF_LIST[random_hand]   
    return hand