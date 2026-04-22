import random
import csv

def grouping(import_file, export_file, accuracy):
    player_pool=[]

    with open(import_file, mode='r', encoding="utf-8") as infile:
        reader = csv.reader(infile, delimiter=';', quotechar='|')
        for row in reader:
            # skip empty or malformed rows
            if not row or len(row) < 2:
                continue

            # optional: skip rows with empty fields
            if not row[0].strip() or not row[1].strip():
                continue

            player_pool.append(row)

    # print(player_pool)

    rating_sum = 0
    for player in player_pool:
        rating_sum += int(player[1])

    avrg_rating = rating_sum/len(player_pool)

    # print(rating_sum, len(player_pool), avrg_rating)
    # print(player_pool)
    # breakpoint()


    def swap_players(group1, group2):
            # Randomly select a player from each group
        player1 = random.choice(group1)
        player2 = random.choice(group2)
        print(player1,player2)
            # Swap the players between groups
        group1.remove(player1)
        group2.remove(player2)
        group1.append(player2)
        group2.append(player1)


    def calculate_average_rating(group):
        ratings = [int(player[1]) for player in group]
        return sum(ratings) / len(ratings)


    def group_players(player_pool):
        random.shuffle(player_pool)
        group_list = []
        new_group = []
            # populate initial group_list
        for x in range (0,len(player_pool)):
            if x % 3 == 0 and x!=0:
                group_list.append(new_group)
                new_group = []
            new_group.append(player_pool[x])
        group_list.append(new_group)

        # Fill incomplete groups with subs
        sub_candidates = [player_pool[0], player_pool[3]]

        sub_index = 0

        for group in group_list:
            while len(group) < 3:
                sub_player = sub_candidates[sub_index]
                sub_index += 1

                sub_player_copy = [sub_player[0] + " (sub)", sub_player[1]]
                group.append(sub_player_copy)

        return(group_list)


    def main(groups):
        num_iterations = accuracy  # Adjust as needed
        best_avg_diff = float('inf')
        best_groups = groups[:]
        
            # Calculate overall average rating
        overall_avg_rating = avrg_rating


        for _ in range(num_iterations):
                # Randomly select two groups
            group_indices = random.sample(range(len(groups)), 2)
            group1, group2 = groups[group_indices[0]], groups[group_indices[1]]
            
                # Calculate initial average ratings
            initial_avg_rating1 = calculate_average_rating(group1)
            initial_avg_rating2 = calculate_average_rating(group2)
            initial_avg_diff = abs(initial_avg_rating1 - overall_avg_rating) + abs(initial_avg_rating2 - overall_avg_rating)
            
                # Randomly select two players to swap
            player1 = random.choice(group1)
            player2 = random.choice(group2)
            
                # Swap players between groups
            group1.remove(player1)
            group2.remove(player2)
            group1.append(player2)
            group2.append(player1)
            
                # Calculate new average ratings
            new_avg_rating1 = calculate_average_rating(group1)
            new_avg_rating2 = calculate_average_rating(group2)
            new_avg_diff = abs(new_avg_rating1 - overall_avg_rating) + abs(new_avg_rating2 - overall_avg_rating)
            
                # Check if the swap improves the balance
            if new_avg_diff < initial_avg_diff:
                if new_avg_diff < best_avg_diff:
                    best_avg_diff = new_avg_diff
                    best_groups = groups[:]
            else:
                    # Revert the swap
                group1.remove(player2)
                group2.remove(player1)
                group1.append(player1)
                group2.append(player2)
        
        return best_groups

    grouped_players = group_players(player_pool)

    new_grouped_players = main(grouped_players)

    with open(export_file, mode='a+', encoding="utf-8") as f:
        for i, group in enumerate(new_grouped_players):
            # print(f"Team {i+1}: {group}, rating: , {round(calculate_average_rating(group),2)}")

            f.write(f"Team {i+1}: {group}, rating: {round(calculate_average_rating(group),2)}" + '\n')
        f.write("--- " + '\n')

    # print(new_grouped_players)
    return new_grouped_players


# grouping("Dresden_Debacle_Registrations_5.csv","team_shuffel.txt", 1000)