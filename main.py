from load_web import load_web
from manual_input import manual_input
import sys
from itertools import combinations
from valid_file_name import valid_file_name


def free_agent_count(lst):
    return [p.is_free_agent for p in lst].count(True)


def get_average_rating(lst):
    return sum(list(map(lambda p: p.get_rating, lst))) / len(lst)


def get_average_strength(lst):
    return sum([p.get_stregth for p in lst]) / len(lst)


def output_lst(lst):
    out = ""
    for p in lst:
        #problem: long names
        out += "{0} ({1})\t".format(p.name, p.rating)
    return out


def filter_players(lst, mask=[None, None, None, None]):
    for i in range(len(mask)):
        if mask[i] != None and lst[i] != mask[i]:
            return False
    return True


def main():
    players = []

    if len(sys.argv) == 1:
        # default if no command line arguments provided
        players = manual_input()
    elif sys.argv[1] == "-manual":
        players = manual_input()
    elif sys.argv[1] == "-load":
        url = None
        if len(sys.argv) > 2:
            url = sys.argv[2]
        players = load_web(url)

    # method = ""
    # while not (method in ["load", "manual"]):
    #     print("Type \'load\' to load player data from the Internet.")
    #     print("Type \'manual\' to enter player data manually.")
    #     method = input(">> ").strip()


    # fix boards
    board_choices = [None, None, None, None]

    if input("Would you like to fix boards? (y/n)\n>>").strip() == "y":
        print("Please enter player's last name.")
        print("Hit Enter if no preference for that board")
        for i in range(4):
            inp = input("Board {0}: ".format(i+1)).strip()
            if inp != "":
                for p in players:
                    if inp.upper() in p.name.upper().split(" "):
                        #simply picks the first player with that name
                        board_choices[i] = p
                        break


    #minimum and maximum conditions
    min_rating = -1
    while not (2000 <= min_rating < 2500):
        try:
            min_rating = int(input("Please enter desired minimum average rating.\n>> "))
        except ValueError:
            continue

    max_rating = 2500

    combs = combinations(players, 4)

    valid_combs = []
    comb_count = 0

    print("Possible combinations:")
    for c in combs:
        avg = get_average_rating(c)
        strength_avg = get_average_strength(c)

        if min_rating <= avg < max_rating and free_agent_count(c) < 2 and filter_players(c, board_choices):
            comb_count += 1
            valid_combs.append([c, avg, strength_avg])

            print(output_lst(c), avg, strength_avg)

    valid_combs.sort(key=lambda c: -c[1]) #sort by avg rating (high to low)
    n = min(len(valid_combs), 10) #in case there are less than 10 combinations
    print("\nThe {0} best combinations are:".format(n))
    for i in range(n):
        print(output_lst(valid_combs[i][0]), valid_combs[i][1], valid_combs[i][2])


    #TODO: 3 OPTIONS: Display best, display all, write to excel

    if input("Write to Excel (y/n)?\n>> ").strip() == "y":
        import xlsxwriter as xw

        file_name = ""
        while not valid_file_name(file_name):
            file_name = input("Please enter file name.\n>> ").strip()

        wb = xw.Workbook(file_name + ".xlsx")
        ws1 = wb.add_worksheet("Combinations")
        ws2 = wb.add_worksheet("Players")

        title = wb.add_format({'bold': True})

        for i in range(4):
            ws1.write(0, i, "Board {0}".format(i+1), title)
        ws1.write(0, 4, "Avg Rating", title)
        ws1.write(0, 5, "Avg Strength", title)

        row1 = 1
        col1 = 0
        for c, a, s in valid_combs:
            for p in c:
                ws1.write(row1, col1, "{0} ({1}; {2})".format(p.name, p.rating, p.get_stregth))
                col1 += 1
            ws1.write(row1, col1, a)
            ws1.write(row1, col1+1, s)
            col1 = 0
            row1 += 1

        #hopefully there is no player with a super long name who isn't in the combinations
        max_len = max([len(p.name) for p in players])
        ws1.set_column(0, 3, max_len + 10)
        ws1.set_column(4, 5, 12)

        ws2.write(0, 0, "Player Name", title)
        ws2.write(0, 1, "Rating", title)
        ws2.write(0, 2, "Strength", title)
        ws2.write(0, 3, "Status", title)
        ws2.write(0, 4, "Gender", title)

        row2 = 1
        col2 = 0
        for p in players:
            ws2.write(row2, col2, p.name)
            col2 += 1
            ws2.write(row2, col2, p.rating)
            col2 += 1
            ws2.write(row2, col2, p.get_stregth)
            col2 += 1
            ws2.write(row2, col2, p.is_free_agent)
            col2 += 1
            ws2.write(row2, col2, p.is_female)
            col2 = 0
            row2 += 1

        ws2.set_column(0, 0, max_len)

        wb.close()


if __name__ == "__main__":
    main()
    print("May the best team (SJH) win!")
