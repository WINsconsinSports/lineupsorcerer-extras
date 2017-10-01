#
# This script takes input of a Draft Kings contest standings zip file
# and outputs the lineups formatted in position order into output.csv.
#
# See the README for usage information.
#
# WINsconsinSports
#
import pandas as pd
import re
# csv of form:
# Rank,EntryId,EntryName,TimeRemaining,Points,Lineup
file_name="contest-standings.zip"
parsed_results=pd.read_csv(file_name)
POSITIONS=["QB","RB","WR","TE","FLEX","DST"]


lineup_list = []
for lineup in parsed_results['Lineup'].dropna():
    # Each lineup is listed in the "Lineup" column in the form:
    # POSITION FirstName LastName POSITION FirstNameLastName ...

    # Split on valid positions (keeping positions in the result)
    lineup_components = re.split('(QB|RB|WR|TE|FLEX|DST)', lineup)

    # Remove first element if it is empty (it will be)
    if not lineup_components[0]:
        lineup_components = lineup_components[1:]

    # Since the later logic relies on a list of tuples with (position, player),
    # force our data into that form (lazy).
    lineup_list.append(
        [tuple(lineup_components[i:i+2]) for i in range(0, len(lineup_components), 2)]
    )

csv_output = 'user,points,qb,rb1,rb2,wr1,wr2,wr3,te,flex,dst\n'
for idx, lineup in enumerate(lineup_list):
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

    csv_output += f"{parsed_results['EntryName'][idx]},{parsed_results['Points'][idx]},"
    # Loop over POSITIONS specified above and add the
    # position,player to the csv storage string (written as file later).
    for pos in POSITIONS:
        for player_at_pos in formatted_lineup[pos]:
            csv_output += f"{player_at_pos.strip(' ')},"
    csv_output += '\n'

with open('output.csv', 'w') as out_file:
    out_file.write(csv_output)
