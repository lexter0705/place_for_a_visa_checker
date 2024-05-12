import json


def get_data_for_web_bot():
    with open("../spain/spain_telegram_bot/settings/web_bot.json", encoding="utf-8", mode="r") as read_file:
        data = json.load(read_file)

    return data


def get_data_for_sender_telegram_bot():
    with open("../spain/spain_telegram_bot/settings/sender_bot.json", encoding="utf-8", mode="r") as read_file:
        data = json.load(read_file)

    return data


def get_data_for_telegram_bot():
    with open("../spain/spain_telegram_bot/settings/telegram_bot.json", encoding="utf-8", mode="r") as read_file:
        data = json.load(read_file)

    return data
