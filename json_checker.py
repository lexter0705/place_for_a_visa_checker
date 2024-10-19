import json


def get_data_for_parser():
    with open("settings/parser.json", encoding="utf-8", mode="r") as read_file:
        data = json.load(read_file)

    return data