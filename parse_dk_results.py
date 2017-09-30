#
# This script takes input of a Draft Kings contest standings zip file
# and outputs the lineups formatted in position order into output.csv.
#
# Step 1) Change the file_name variable below to the file name
# of the contest standings zip file you have downloaded.
# 
# Step 2) run this script
# 
# Step 3) HAVE FUN!
#
# WINsconsinSports
#
import pandas as pd
import re
# csv of form:
# Rank,EntryId,EntryName,TimeRemaining,Points,Lineup
file_name="contest-standings-45286830.zip"
player_lineups=pd.read_csv(file_name)
POSITIONS=["QB","RB","WR","TE","FLEX","DST"]
lineup_list=[]
for idx, lineup in enumerate(player_lineups['Lineup'].dropna()):
    # Each lineup is listed in the "Lineup" column in the form:
    # POSITION FirstName LastName POSITION FirstNameLastName ...
    regex = "([A-Z][A-Z]+)\s([\w'.]*[\s][\w]*)"
    parsed_lineup = re.findall(regex, lineup)
    lineup_list.append(parsed_lineup)

csv_output = 'position,player\n'
for lineup in lineup_list:
    formatted_lineup = {}
    # The lineup is now a list of tuples containing
    # position and player in the form of:
    # [(POSITION, PLAYER), (POSITION, PLAYER) ...].
    # Add each player/defense to a dictionary with the
    # lineup position as the key.
    for filled_position in lineup:
        if filled_position[0] in formatted_lineup:
            # add to list of players at that position
            formatted_lineup[filled_position[0]].append(filled_position[1])
        else:
            # position not added to lineup yet, add it (list form).
            formatted_lineup[filled_position[0]] = [filled_position[1]]
    
    # Loop over POSITIONS specified above and add the
    # position,player to the csv storage string (written as file later).
    for pos in POSITIONS:
        for player_at_pos in formatted_lineup[pos]:
            csv_output += f"{pos},{player_at_pos}"
            csv_output += '\n'
    csv_output += '\n'

with open('output.csv', 'w') as out_file:
    out_file.write(csv_output)
  