import cnfg
import models
import pprint as pp

def log_biggest_losses(log_text):
    path = 'data/training/logs/'
    f = open("logfile.txt", "a")
    f.write(log_text)
    f.close()

def output_model_predictions(model):

    fold_list = []
    call_list = []
    raise_list = []
    rai_list = []

    for hand in cnfg.SF_LIST:

        oheh = model.encode_hand(hand,[])
    
        output = model(oheh)

        action = models.action_taken_by_model(output)

        if action == 0:
            fold_list.append(hand)
        elif action == 1:
            call_list.append(hand)
        elif action == 2:
            raise_list.append(hand)
        elif action == 3:
            rai_list.append(hand)

    print("Fold:")
    pp.pprint(fold_list)
    print("Call:")
    pp.pprint(call_list)
    print("Raise:")
    pp.pprint(raise_list)
    print("rai:")
    pp.pprint(rai_list)

