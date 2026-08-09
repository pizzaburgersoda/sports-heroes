import csv

def readcsvdata(tournament_name):
    filename = tournament_name + ".csv"
    with open(filename, mode="r") as file:
        csvFile = csv.DictReader(file)
        tournament_data = list(csvFile)
    return tournament_data

def initialize():
    filename = "analysis.dat"
    with open(filename, mode="w") as file:
        file.write("Analysis Results\n")

def print_line(report_line):
    filename = "analysis.dat"
    with open(filename, mode="a") as file:
        file.write(report_line)

def print_table(table):
    filename = "analysis.dat"
    with open(filename, mode="a") as file:
        # Print headers normally, but streak header aligned to the right
        all_keys = list(table[0].keys())
        keys_line = " "
        for key in all_keys:
            if key != "Longest Streak":  # skip streak for now
                keys_line += key + (25 - len(key)) * " "
        # Pad line to 115 chars, then add streak header
        keys_line = keys_line.ljust(115) + "Longest Streak"
        file.write(keys_line + "\n")

        # Print values
        for data in table:
            value_lines = " "
            for key in all_keys:
                if key != "Longest Streak":
                    values = data[key]
                    value_lines += str(values) + (25 - len(str(values))) * " "
            # Pad line to 115 chars, then add streak value
            streak_value = str(data["Longest Streak"])
            value_lines = value_lines.ljust(115) + streak_value
            file.write(value_lines + "\n")


def print_set(winner_set):
    filename = "analysis.dat"
    with open(filename, mode="a") as file:
        for winner in winner_set:
            file.write(winner + ",")
        file.write("\n\n")

# -------------------------------
# Enhancements
# -------------------------------

def longest_streak(years):
    years = sorted([int(y) for y in years])
    streak, max_streak = 1, 1
    for i in range(1, len(years)):
        if years[i] == years[i-1] + 1:
            streak += 1
            max_streak = max(max_streak, streak)
        else:
            streak = 1
    return max_streak

def country_analysis(winners_info_list):
    country_dict = {}
    for player in winners_info_list:
        country = player["Country"]
        country_dict.setdefault(country, []).append(player["Name"])
    print_line("\nCountry Analysis:\n")
    for country, players in country_dict.items():
        print_line(country + ": " + ", ".join(players) + "\n")

def analyze(tname, tdata):
    winners_list = [winner["Champion"] for winner in tdata]
    winners_set = set(winners_list)

    print_line("\nReporting for " + tname + "\n")
    print_line("Total Winners: " + str(len(winners_list)) + "\n")
    print_line("Unique Winners: " + str(len(winners_set)) + "\n")

    winners_info_list = []
    for player in winners_set:
        selected = [chosen for chosen in tdata if chosen["Champion"] == player]
        years_won = [kk["Year"] for kk in selected]

        player_info = {
            "Name": player,
            "Country": selected[0]["Country"],
            "Times Won": len(selected),
            "Years Won": years_won,
            "Longest Streak": longest_streak(years_won)  # now horizontal
        }
        if "RunnerUp" in selected[0]:
            player_info["Runners-Up"] = [kk["RunnerUp"] for kk in selected]

        winners_info_list.append(player_info)

    # Sort results by Times Won
    winners_info_list = sorted(winners_info_list, key=lambda x: x["Times Won"], reverse=True)

    # Print table including streak as its own column
    print_table(winners_info_list)

    # Country-centric analysis
    country_analysis(winners_info_list)

    # Multiple-time winners
    mto_winners_set = {p["Name"] for p in winners_info_list if p["Times Won"] > 1}
    return winners_set, mto_winners_set

# -------------------------------
# Comparative functions
# -------------------------------

def union_sets(*sets):
    return set().union(*sets)

def intersection_sets(*sets):
    return set.intersection(*sets)

def only_one_tournament(*sets):
    all_union = union_sets(*sets)
    all_intersection = intersection_sets(*sets)
    return all_union - all_intersection

def symmetric_difference_sets(*sets):
    result = sets[0]
    for s in sets[1:]:
        result = result ^ s
    return result

def comparative_analysis(winner_set1, winner_set2):
    winner_eitheror = union_sets(winner_set1, winner_set2)
    winner_both = intersection_sets(winner_set1, winner_set2)
    winner_only_wimbledon = winner_set1 - winner_set2
    winner_only_frenchopen = winner_set2 - winner_set1
    winner_only_1_not_both = symmetric_difference_sets(winner_set1, winner_set2)

    print_line("\nComparative Analysis:\n")
    print_line("Winners (Either/Or): " + str(len(winner_eitheror)) + "\n")
    print_set(winner_eitheror)

    print_line("Winners (Both): " + str(len(winner_both)) + "\n")
    print_set(winner_both)

    print_line("Winners (Only Wimbledon): " + str(len(winner_only_wimbledon)) + "\n")
    print_set(winner_only_wimbledon)

    print_line("Winners (Only French Open): " + str(len(winner_only_frenchopen)) + "\n")
    print_set(winner_only_frenchopen)

    print_line("Winners (Only 1, not both): " + str(len(winner_only_1_not_both)) + "\n")
    print_set(winner_only_1_not_both)

# -------------------------------
# MAIN EXECUTION
# -------------------------------

initialize()
Wimbledon_data = readcsvdata("Wimbledon")
FrenchOpen_data = readcsvdata("FrenchOpen")

wimbledon_winners, wimbledon_mto_winners = analyze("Wimbledon", Wimbledon_data)
frenchopen_winners, frenchopen_mto_winners = analyze("French Open", FrenchOpen_data)

comparative_analysis(wimbledon_winners, frenchopen_winners)
