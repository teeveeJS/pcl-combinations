import urllib.request
import re
from itertools import combinations

class Player:
    def __init__(self, n, r, fa=False, is_f=False):
        self.name = n
        self.rating = int(r)
        #these should be type-casted to bools
        self.is_free_agent = fa
        self.is_female = is_f

    @property
    def get_rating(self):
        if self.rating > 2700:
            return 2700
        elif self.rating < 2000:
            return 2000
        else:
            return self.rating

def free_agent_count(lst):
    return sum(list(map(lambda p: p.is_free_agent, lst)))

def get_average_rating(lst):
    return sum(list(map(lambda p: p.get_rating, lst))) / len(lst)

def has_female(lst):
    return bool(sum(list(map(lambda p: p.is_female, lst))))

def output_lst(lst):
    out = ""
    for p in lst:
        #problem: long names
        out += "{0} ({1})\t".format(p.name, p.rating)
    return out

def main():
    players = []

    method = ""
    while not (method in ["load", "manual"]):
        print("Type \'load\' to load player data from the Internet.")
        print("Type \'manual\' to enter player data manually.")
        method = input(">> ").strip()

    if method == "load":
        url = input("Please enter url\n>> ").strip()
        conn = urllib.request.urlopen(url)

        data = conn.read()

        name_data = re.findall(r'target="_blank">(.*?)</td>', str(data))
        # for d in name_data:
        #     print(d)
        rtg_data = re.findall(r'>(\d{4}?)</td>', str(data))
        # for r in rtg_data:
        #     print(r)

        #TODO: free_agent

        #currently no way of knowing whether the player is a free agent or female

        for i in range(len(name_data)):
            players.append(Player(name_data[i], rtg_data[i]))
    else:
        print("Type \'exit\' when done.")
        while True:
            new_player = input("LASTNAME RATING [ISFREEAGENT] [ISFEMALE]\n>> ").split(" ")

            if new_player[0] == "exit":
                break

            #TODO: implement some input control

            print("{0} added!".format(new_player[0]))
            players.append(Player(*new_player))

    #minimum and maximum conditions
    min_rating = int(input("Please enter desired minimum average rating.\n>> "))
    max_rating = 2500

    combs = combinations(players, 4)

    valid_combs = []
    comb_count = 0

    print("Possible combinations:")
    for c in combs:
        avg = get_average_rating(c)

        #bonus to the maximum average if the team contains a female player
        add = 0
        if has_female(c):
            add = 10

        if min_rating <= avg <= max_rating + add and free_agent_count(c) < 2:
            comb_count += 1
            valid_combs.append([c, avg])

            print(output_lst(c), avg)

    valid_combs.sort(key=lambda c: -c[1]) #sort by avg rating (high to low)
    n = min(len(valid_combs), 10) #in case there are less than 10 combinations
    print("\nThe {0} best combinations are:".format(n))
    for i in range(n):
        print(output_lst(valid_combs[i][0]), valid_combs[i][1])


if __name__ == "__main__":
    main()
