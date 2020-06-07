import sys

from instabot import InstaBot
import json
import main

if __name__ == '__main__':

    command = sys.argv[1]
    if command == '-launch':

        path_to_cfg = sys.argv[2]
        with open(path_to_cfg) as f:
            x = f.read()
        args = json.loads(x)
        bot = InstaBot(**args)

        print(' _____              _    _  _    _       ___   _ \n'
              '|_   _|            | |  | || |  | |     / _ \ | |\n'
              '  | |   _ __   ___ | |_ | || |_ | |__  | | | || |_ \n'
              '  | |  |  _ \ / __|| __||__   _|| |_ \ | | | || __|\n'
              ' _| |_ | | | |\__ \| |_    | |  | |_) || |_| || |_\n'
              '|_____||_| |_||___/ \__|   |_|  |_|__/  \___/  \__|  v1.0\n')
        print('[->] launching Inst4b0t...')
        bot.start_session()

    elif command == '-analyze':
        print('[->] showing analysis...')
        main.main.run(debug=True)
    elif command == '-help' or command == '-?':
        print('[1] Bot launch: \n'
              '> python driver.py -launch -path_to_cfg [json format]')
        # (Maja) dopiszcie sobie reszte helpa
    else:
        print('[!] \'' + command + '\' is unknown argument.')
