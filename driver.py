import sys

from instabot import InstaBot
import json
import main
import matplotlib.pyplot as plt

def main():
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
        username = sys.argv[2]
        print('[->] showing analysis...')
        main.main.run(debug=True)
        data = []
        db = shelve.open('db')
        if db.items == []:
            print('brak danych!')
            return
        for x in db.items():
            date,username = x[0].split('||')
            dates = []
            follows = []
            likes = []
            following = []
            posts = []
            comments = []
            if usermane.rstrip().lstrip() == username:
                dates.append(date)
                follows.append(x[1]['followers_count'])
                following.append(x[1]['following_count'])
                posts.append(x[1]['post_count'])
                likes.append(x[1]['average_post_likes'])
                comments.append(x[1]['comments_analysis'])
        plot = plt.figure()
        subplot1 = plot.add_subplot()
        subplot1.scatter(dates,follows,label='followers')
        subplot1.scatter(dates,likes,label='average post likes')
        subplot1.scatter(dates,following,label='following')
        subplot1.scatter(dates,posts,label='post count')
        subplot1.scatter(dates,comments,label='comments analisys')
        plt.show()
        
    elif command == '-help' or command == '-?':
        pass
    else:
        print('[!] \'' + command + '\' is unknown argument.')

if __name__ == '__main__':
    main()
    