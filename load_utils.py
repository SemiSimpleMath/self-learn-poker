import player
import models
import loss_functions

def load_multiple_players(path):

    import os

    files = os.listdir(path)

    count = 0
    player_list = []
    for f in files:
        P = player.Player(models.ModelPlayer, loss_functions.RMSELoss, count)
        P.load_model(path+f)
        count += 1

        player_list.append(P)
   

    return player_list
    
