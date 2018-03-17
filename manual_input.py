def manual_input():
    from player import Player

    players = []

    print("Type \'exit\' when done.")
    while True:
        new_player = input("LASTNAME RATING [ISFREEAGENT] [ISFEMALE]\n>> ").split(" ")

        if new_player[0] == "exit":
            break

        try:
            new_player[1] = int(new_player[1])
        except (ValueError, IndexError):
            continue

        try:
            if new_player[2].upper() == "TRUE":
                new_player[2] = True
            elif new_player[2].upper() == "FALSE":
                new_player[2] = False
        except IndexError:
            new_player.append(False)

        try:
            if new_player[3].upper() == "TRUE":
                new_player[3] = True
            elif new_player[3].upper() == "FALSE":
                new_player[3] = False
        except IndexError:
            new_player.append(False)

        try:
            players.append(Player(*new_player))
            print("{0} added!".format(new_player[0]))
        except AssertionError:
            print("An error occurred: no player added.")

    return players
