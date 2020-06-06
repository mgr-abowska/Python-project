import sys
from instabot import InstaBot
import json

if __name__ == '__main__':

      command = sys.argv[1]
      if command == '-launch':
            path_to_cfg = sys.argv[2]
            # (Kapitan) zaladuj tutaj jsona
            with open(path_to_cfg) as f:
                  x = f.read()
            args = json.load(x)
            bot = InstaBot(**args)
            print(' _____              _    _  _    _       ___   _ \n'
                  '|_   _|            | |  | || |  | |     / _ \ | |\n'
                  '  | |   _ __   ___ | |_ | || |_ | |__  | | | || |_ \n'
                  '  | |  |  _ \ / __|| __||__   _|| |_ \ | | | || __|\n'
                  ' _| |_ | | | |\__ \| |_    | |  | |_) || |_| || |_\n'
                  '|_____||_| |_||___/ \__|   |_|  |_|__/  \___/  \__|  v1.0\n')
            print('[->] launching Inst4b0t...')

            # (Kapitan) ustawiasz parametry w insta bocie z json'a
            #  InstaBot.comments = [scrap z jsona] (Wszystkie parametry potrzebne masz w konstruktorze)
            bot.start_session() # bot od tego momentu sobie sam radzi

      elif command == '-analyze':
            print('[->] showing analysis...')
            # (Maja) format DATA_POCZATKOWA : DATA_KONCOWA analiza
      elif command == '-help' or command == '-?':
            print('[1] Bot launch: \n'
                  '> python driver.py -launch -path_to_cfg [json format]')
            # (Maja) dopiszcie sobie reszte helpa
      else:
            print('[!] \'' + command + '\' is unknown argument.')

