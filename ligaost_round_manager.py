import csv
import os
import random
from datetime import datetime
from ligaost_team_shuffel import grouping  # your existing function
import shutil

def ensure_history_folder():
    folder = "round_history"
    if not os.path.exists(folder):
        os.makedirs(folder)
    return folder

def has_sub(team):
    return any("(sub)" in player[0] for player in team)

def write_round(player_file, round_file, accuracy):
    import csv
    import os
    import random
    from datetime import datetime

    # archive old file
    history_folder = ensure_history_folder()

    if os.path.exists(round_file):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        os.rename(
            round_file,
            os.path.join(history_folder, f"round_{timestamp}.csv")
        )

    groups = grouping(player_file, "team_shuffel.txt", accuracy)

    def normalize(name):
        return name.replace(" (sub)", "")

    def teams_overlap(team1, team2):
        names1 = {normalize(p[0]) for p in team1}
        names2 = {normalize(p[0]) for p in team2}
        return not names1.isdisjoint(names2)

    max_attempts = 100
    valid = False

    for _ in range(max_attempts):
        random.shuffle(groups)

        pairings = []
        valid = True

        # normal pairings
        for i in range(0, len(groups) - 1, 2):
            team1 = groups[i]
            team2 = groups[i + 1]

            if teams_overlap(team1, team2):
                valid = False
                break

            pairings.append((team1, team2))

        if not valid:
            continue

        # handle odd team
        if len(groups) % 2 == 1:
            extra_team = groups[-1]

            valid_targets = [
                team for team in groups[:-1]
                if not has_sub(team) and not teams_overlap(extra_team, team)
            ]

            if valid_targets:
                opponent = random.choice(valid_targets)
            else:
                # fallback: allow overlap if unavoidable
                opponent = random.choice(groups[:-1])

            pairings.append((extra_team, opponent))

        # if we got here → valid pairing found
        break

    if not valid:
        print("Warning: Could not avoid overlap, using last pairing")

    # write file
    with open(round_file, mode="w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, delimiter=';')

        writer.writerow(["Team1", "Players1", "vs", "Team2", "Players2", "Score"])

        team_counter = 1

        for team1, team2 in pairings:
            players1 = ", ".join([p[0] for p in team1])
            players2 = ", ".join([p[0] for p in team2])

            writer.writerow([
                f"Team {team_counter}",
                players1,
                "vs",
                f"Team {team_counter + 1}",
                players2,
                "0:0"
            ])

            team_counter += 2
    

def expected_score(r1, r2):
    return 1 / (1 + 10 ** ((r2 - r1) / 400))


def update_ratings_from_round(player_file, round_file, k):

    # archive old file
    history_folder = ensure_history_folder()

    if os.path.exists(player_file):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = os.path.join(
            history_folder,
            f"players_{timestamp}.csv"
        )

        shutil.copy(player_file, backup_file)


    # load players into dict
    players = {}
    with open(player_file, mode="r", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=';')
        for row in reader:
            # skip invalid rows
            if not row or len(row) < 2:
                continue

            name = row[0].strip()
            rating = row[1].strip()

            if not name or not rating:
                continue

            players[name] = float(rating)

    # read round file
    with open(round_file, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=';')

        for row in reader:
            score = row["Score"]
            if ":" not in score:
                continue

            s1, s2 = map(int, score.split(":"))

            team1_players = [p.strip() for p in row["Players1"].split(",")]
            team2_players = [p.strip() for p in row["Players2"].split(",")]

            # remove "(sub)" suffix
            team1_players = [p.replace(" (sub)", "") for p in team1_players]
            team2_players = [p.replace(" (sub)", "") for p in team2_players]

            # compute team ratings
            r1 = sum(players[p] for p in team1_players) / len(team1_players)
            r2 = sum(players[p] for p in team2_players) / len(team2_players)

            e1 = expected_score(r1, r2)
            e2 = expected_score(r2, r1)

            # actual result
            if s1 > s2:
                a1, a2 = 1, 0
            elif s1 < s2:
                a1, a2 = 0, 1
            else:
                a1, a2 = 0.5, 0.5

            # update players
            for p in team1_players:
                players[p] += k * (a1 - e1)

            for p in team2_players:
                players[p] += k * (a2 - e2)

    # write back to file
    with open(player_file, mode="w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, delimiter=';')
        for name, rating in players.items():
            writer.writerow([name, round(rating)])