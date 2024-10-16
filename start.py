from register_bot import main as telegram_bot
from parser import parser as web_script
from multiprocessing import Process
from database import creator


def start():
    bot = Process(target=telegram_bot.start)
    web = Process(target=web_script.start)
    bot.start()
    web.start()
    bot.join()
    web.join()


def create_db():
    creator.start()


if __name__ == "__main__":
    start()
