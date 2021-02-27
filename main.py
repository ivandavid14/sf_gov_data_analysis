import csv
import os
import re
import string

from collections import namedtuple
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

def main():
    file_path = Path("sfgov_legislation") / "dean_preston_voting_record.csv"
    voting_record = VotingRecord("Dean Preston", file_path)
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

if __name__ == "__main__":
    main()
