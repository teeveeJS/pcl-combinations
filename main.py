import urllib.request
import http.client
import re
from itertools import combinations
from valid_file_name import valid_file_name


class Player:
    def __init__(self, n, r, fa=False, is_f=False):
        self.name = n
        self.rating = int(r)

        #these should be type-casted to bools
        self.is_free_agent = fa
        self.is_female = is_f

    @property
    def get_rating(self):
        rtg = self.rating - int(self.is_female) * 100
        return max(2000, min(2700, rtg))


def free_agent_count(lst):
    return [p.is_free_agent for p in lst].count(True)


def get_average_rating(lst):
    return sum(list(map(lambda p: p.get_rating, lst))) / len(lst)


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

    method = ""
    while not (method in ["load", "manual"]):
        print("Type \'load\' to load player data from the Internet.")
        print("Type \'manual\' to enter player data manually.")
        method = input(">> ").strip()

    if method == "load":
        url = input("Please enter url.\n>> ").strip()
        conn = urllib.request.urlopen(url)

        data = str(conn.read())

        # name and rating data and a bunch of extraneous stuff from regex
        n_r = re.findall(r'(target="_blank">(.*?)</td>|>(\d{4}?)</td>)', data)

        player_names = []
        player_ratings = []
        # filter out the useless info
        # most importantly, the performance ratings!!
        for i in range(len(n_r)):
            if n_r[i][0].startswith("target="):
                if n_r[i][1].startswith("Loss") or n_r[i][1].startswith("Win") \
                   or n_r[i][1].startswith("Tie"):
                       break
                player_names.append(n_r[i][1])
                player_ratings.append(int(n_r[i + 1][2]))


        fa = re.findall(r'<td style="text-align: center;">(.*?)</td>', data)
        free_agents = []
        for s in fa:
            if s == "Free Agent":
                free_agents.append(True)
            elif s == "Local" or s == "Streamer":
                free_agents.append(False)
        # print(free_agents)

        gender_data = []
        for name in player_names:
            print(name)

            h1 = http.client.HTTPConnection("ratings.fide.com")
            h1.request("GET", "/search.phtml?search={0}".format(name.replace(" ", "%2C+")), headers={})#headers=headers)
            page_data = h1.getresponse().read()

            m_or_f = re.findall(r'<td>&nbsp;([M, F])</td>|$', str(page_data))[0]

            if m_or_f == "F":
                gender_data.append(True)
            else:
                # there is a possibility that m_or_f == "" (player not found in fide database)
                # program operates under the assumption that this player is not female
                gender_data.append(False)

        if len(player_names) != len(free_agents):
            raise ValueError("Error in counting players. One player may not have a chess.com account. Sorry, try \'manual\' mode.")

        for i in range(len(player_names)):
            players.append(Player(player_names[i], player_ratings[i], free_agents[i], gender_data[i]))
    else:
        print("Type \'exit\' when done.")
        while True:
            new_player = input("LASTNAME RATING [ISFREEAGENT] [ISFEMALE]\n>> ").split(" ")

            if new_player[0] == "exit":
                break

            #TODO: implement some input control

            print("{0} added!".format(new_player[0]))
            players.append(Player(*new_player))


    # fix boards
    board_choices = [None, None, None, None]

    if input("Would you like to fix boards? (y/n)\n>>").strip() == "y":
        print("Please enter player's last name.")
        print("Just hit Enter if no preference for that board")
        for i in range(4):
            inp = input("Board {0}: ".format(i+1)).strip()
            if inp != "":
                for p in players:
                    if inp.upper() in p.name.upper().split(" "):
                        #simply picks the first player with that name
                        board_choices[i] = p
                        break


    #minimum and maximum conditions
    min_rating = int(input("Please enter desired minimum average rating.\n>> "))
    max_rating = 2500

    combs = combinations(players, 4)

    valid_combs = []
    comb_count = 0

    print("Possible combinations:")
    for c in combs:
        avg = get_average_rating(c)

        if min_rating <= avg < max_rating and free_agent_count(c) < 2 and filter_players(c, board_choices):
            comb_count += 1
            valid_combs.append([c, avg])

            print(output_lst(c), avg)

    valid_combs.sort(key=lambda c: -c[1]) #sort by avg rating (high to low)
    n = min(len(valid_combs), 10) #in case there are less than 10 combinations
    print("\nThe {0} best combinations are:".format(n))
    for i in range(n):
        print(output_lst(valid_combs[i][0]), valid_combs[i][1])


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

        row1 = 1
        col1 = 0
        for c, a in valid_combs:
            for p in c:
                ws1.write(row1, col1, "{0} ({1})".format(p.name, p.rating))
                col1 += 1
            ws1.write(row1, col1, a)
            col1 = 0
            row1 += 1

        #hopefully there is no player with a super long name who isn't in the combinations
        max_len = max([len(p.name) for p in players])
        ws1.set_column(0, 3, max_len + 10)
        ws1.set_column(4, 4, 10)

        ws2.write(0, 0, "Player Name", title)
        ws2.write(0, 1, "Rating", title)
        ws2.write(0, 2, "Status", title)
        ws2.write(0, 3, "Gender", title)

        row2 = 1
        col2 = 0
        for p in players:
            ws2.write(row2, col2, p.name)
            col2 += 1
            ws2.write(row2, col2, p.rating)
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
