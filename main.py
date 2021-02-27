"""CSV analyzer

Usage:
    main.py filter_for_housing_votes <name_with_underscores>
    main.py get_overlap <supervisor_1> <supervisor_2>
"""

import csv
import os
import re
import string

from collections import namedtuple
from docopt import docopt
from pathlib import Path

Action = namedtuple("Action", ["file_number", "action_date", "title", "vote"])

    #file_path = Path("sfgov_legislation") / "dean_preston_voting_record.csv"
def split_records(file_path):
    with open(str(file_path), encoding="utf-8") as f:
        reader = csv.reader(f)
        actions = []
        for action in reader:
            actions.append(Action._make(action))
    
    #For sorting on time if we want
    for action in actions[1:]:
        split = action.action_date.split("/")
        new_datetime_str = f"{split[2]}-{split[1]}-{split[0]}"
        action = action._replace(action_date=new_datetime_str)

    return actions[1:]

StreetName = namedtuple("StreetName", ["full", "name", "type", "post_direction"])

STREET_ACRONYM_TO_FULL = {
    'PL': "place",
    'BLVD': "boulevard",
    'STPS': "steps",
    'HWY': "highway",
    'ROW': "row",
    'ST': "street",
    'TUNL': "tunnel",
    'LOOP': "loop",
    'ALY': "alley",
    'TER': "terrace",
    'PLZ': "plaza",
    'HL': "hill",
    'DR': "drive",
    'WAY': "way",
    'LN': "lane",
    'RAMP': "ramp",
    'CT': "court",
    'AVE': "avenue",
    'EXPY': "expressway",
    'CIR': "circle",
    'RD': "road",
    'PATH': "path",
    'PARK': "park",
    'WALK': "walk"
}

CONFUSING_STREET_NAMES = [
    "a st",
    "d st",
    "r st"
]

def get_street_name(file_path):
    with open(str(file_path), encoding="utf-8") as f:
        reader = csv.reader(f)
        street_names = []
        for row in reader:
            street_names.append(StreetName._make(row))
        
        # fixup
        for street_name in street_names:
            parts = street_name.full.split()
            for part in parts:
                if part in STREET_ACRONYM_TO_FULL:
                    part = STREET_ACRONYM_TO_FULL[part]
            new_full = " ".join(parts)
            street_name = street_name._replace(full=new_full)

    return street_names[1:]

class VotingRecord(object):
    def __init__(self, legislator_name, file_path):
        self._actions = split_records(file_path)
        self.legislator_name = legislator_name

    def find_legislation_referencing_streets(self, street_names):
        lower_case_street_names = [street_name.full.lower() for street_name in street_names]
        for confusing_name in CONFUSING_STREET_NAMES:
            lower_case_street_names.remove(confusing_name)

        retVal = []
        for action in self._actions:
            lowercase_action_title = action.title.lower()
            for street_name in lower_case_street_names:
                if street_name in lowercase_action_title:
                    retVal.append(action)
                    break
        return retVal

    def get_overlap(self, other_voting_record, street_names):
        their_votes = {
            action.file_number: action for action in other_voting_record.find_legislation_referencing_streets(street_names)
        }
        my_overlapping_votes = {
            action.file_number: action for action in self.find_legislation_referencing_streets(street_names) if action.file_number in their_votes
        }

        similar_actions = []
        dissimilar_actions = []
        for file_number, my_action in my_overlapping_votes.items():
            if their_votes[file_number].vote == my_action.vote:
                similar_actions.append(my_action)
            else:
                dissimilar_actions.append((my_action, my_action.vote, their_votes[file_number].vote))
        return (similar_actions, dissimilar_actions)
            

def filter_for_housing_legislation(name):
    file_path = Path("sfgov_legislation") / f"{name}.csv"
    voting_record = VotingRecord(name, file_path)
    street_names = get_street_name(Path("geographic_data") / "street_names.csv")
    actions_with_roads = voting_record.find_legislation_referencing_streets(street_names)

    output_dir = Path("output")
    output_dir.mkdir(parents=True, exist_ok=True)
    ouput_file = (output_dir / voting_record.legislator_name).with_suffix(".csv")
    with ouput_file.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, lineterminator="\n")
        writer.writerow([k for k, _ in actions_with_roads[0]._asdict().items()])
        for action in actions_with_roads:
            writer.writerow(action)

def overlap_votes(supervisor_1, supervisor_2):
    street_names = get_street_name(Path("geographic_data") / "street_names.csv")
    supervisor_1_path = Path("sfgov_legislation") / f"{supervisor_1}.csv"
    supervisor_2_path = Path("sfgov_legislation") / f"{supervisor_2}.csv"

    supervisor_1_record = VotingRecord(supervisor_1, supervisor_1_path)
    supervisor_2_record = VotingRecord(supervisor_2, supervisor_2_path)

    similar_actions, dissimilar_actions = supervisor_1_record.get_overlap(supervisor_2_record, street_names)
    num_actions = len(similar_actions) + len(dissimilar_actions)
    print(f"Number of similar votes: {len(similar_actions)}")
    print(f"Number of dissimilar votes: {len(dissimilar_actions)}")
    print(f"Percentage of agreement amongst actions where they both were elected: %{100 * len(similar_actions) / num_actions : .2f}")
    print(f"Percentage of disagreement amongst actions where they were elected: %{100 * len(dissimilar_actions) / num_actions : .2f}")
    print("------------------------------")

    for dissimilar_action in dissimilar_actions:
        print(dissimilar_action[0].title)
        print(f"{supervisor_1}: {dissimilar_action[1]}")
        print(f"{supervisor_2}: {dissimilar_action[2]}")
        print("----------------------------")

if __name__ == "__main__":
    arguments = docopt(__doc__)
    if arguments["filter_for_housing_votes"]:
        filter_for_housing_legislation(arguments["<name_with_underscores>"])
    elif arguments["get_overlap"]:
        overlap_votes(arguments["<supervisor_1>"], arguments["<supervisor_2>"])

