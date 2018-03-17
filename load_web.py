def load_web(url=None):
    import urllib.request
    import re
    from player import Player

    players = []

    if url is None:
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

    gender_data = []
    strength_data = []
    for name in player_names:
        print(name)

        search_name = name.split(" ")
        search_name = [search_name[-1]] + search_name[:-1]
        search_name = "%2C+".join(search_name)

        player_url = "https://chess-db.com/public/execute.jsp?name={0}&stype=player".format(search_name)
        conn_p = urllib.request.urlopen(player_url)
        page_data = str(conn_p.read())

        try:
            first_hit = re.findall(r'<tr><td>1</td>(.*?)</tr>', str(page_data))[0]

            try:
                strength_data.append(int(re.findall(r'<td>(\d{4}?)</td>', first_hit)[0]))
            except IndexError:
                print("Player {0} rating not found".format(name))
                strength_data.append(None)

            gender_data.append('<td>w </td>' in first_hit or '<td>wi</td>' in first_hit)

        except IndexError:
            print("Player {0} not found".format(name))
            strength_data.append(None)
            gender_data.append(False)


    if len(player_names) != len(free_agents):
        raise ValueError("Error in counting players. One player may not have a chess.com account. Sorry, try \'manual\' mode.")

    for i in range(len(player_names)):
        players.append(Player(player_names[i], player_ratings[i], free_agents[i], gender_data[i], strength_data[i]))

    return players
