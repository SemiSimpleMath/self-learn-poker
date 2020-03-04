
hand_action_log_dict = dict()

def log_hand_and_action(player_1_hand, small_blind, action_list, player_1_outcome):
    global hand_action_log_dict
    if (player_1_hand, small_blind, tuple(action_list)) in hand_action_log_dict:
        total, count = hand_action_log_dict[(player_1_hand, small_blind, tuple(action_list))]
    else:
        total = 0
        count = 0
    count +=1
    total += player_1_outcome
    hand_action_log_dict[(player_1_hand, small_blind, tuple(action_list))] = (total, count)


