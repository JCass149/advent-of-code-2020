input = open("../input/day22.txt").read().splitlines()

player1 = []
player2 = []
player1Active = False
player2Active = False
for inx, line in enumerate(input):
    if line == "Player 1:":
        player1Active = True
    elif line == "Player 2:":
        player2Active = True
    elif line == "":
        continue
    elif player2Active:
        player2.append(int(line))
    else:
        player1.append(int(line))

# make a tuple stack
player1 = tuple(player1)
player2 = tuple(player2)
print("player1: "+str(player1))
print("player2: "+str(player2))
print("")

game = 1


def start_new_game(player1, player2):

    global game
    print("game: "+str(game))
    game += 1
    round = 1
    # set of hisotries
    player1history, player2history = set(), set()

    while True:

        if round <= 2:
            print("round: "+str(round))
            print("player1: "+str(player1))
            print("player2: "+str(player2))
            print("player1history: "+str(player1history))
            print("player2history: "+str(player2history))
        else:
            print("round: "+str(round))

        # check loop condition
        if (player1 in player1history) or (player2 in player2history):
            print("player1: "+str(player1))
            print("player2: "+str(player2))
            print("player1 wins this game due to loop")
            return (player1, "player1")
        else:
            # add these hands to the history
            player1history.add(player1)
            player2history.add(player2)

        player1card, player2card = player1[0], player2[0]
        player1, player2 = player1[1:], player2[1:]

        # check recurse condition
        if len(player1) >= player1card and len(player2) >= player2card:
            winner = start_new_game(
                player1[:player1card], player2[:player2card])
            # if loop:
            # return (winner[0], "player1")
            if winner[1] == "player1":
                player1 = player1 + (player1card, player2card)
            else:
                player2 = player2 + (player2card, player1card)
        # else play as normal
        elif player1card > player2card:
            player1 = player1 + (player1card, player2card)
        else:
            player2 = player2 + (player2card, player1card)

        if len(player1) == 0 or len(player2) == 0:
            break

        round += 1

    print("player1: "+str(player1))
    print("player2: "+str(player2))

    print("end of game "+str(game))
    print("")
    if len(player1) == 0:
        return (player2, "player2")
    else:
        return (player1, "player1")


winner = start_new_game(player1, player2)[0]
print("winner: "+str(winner))
total = 0
for idx, card in enumerate(winner):
    multiplier = len(winner)-idx
    total += multiplier*card

print("total: "+str(total))
