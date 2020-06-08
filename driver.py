import shelve
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
        user = sys.argv[2]
        print('[->] showing analysis...')
        data = []
        db = shelve.open('db')
        if db.items == []:
            print('No data :(')
            db.close()
            return
        dates = []
        follows = []
        likes = []
        following = []
        posts = []
        comments = []
        for x in db.items():
            date, username = x[0].split('||')
            if username.rstrip().lstrip() == user:
                dates.append(date[:date.index('.')])
                follows.append(x[1]['followers_count'])
                following.append(x[1]['following_count'])
                posts.append(x[1]['post_count'])
                likes.append(x[1]['average_post_likes'])
                comments.append(x[1]['comments_analysis'])
        db.close()
        if dates == []:
            print('No data about user: ' + user)
            return
        if len(dates) == 1:
            print('To little data about user: ' + user)
            return
        plt.plot(dates, follows, label='followers')
        plt.plot(dates, likes, label='average post likes')
        plt.plot(dates, following, label='following')
        plt.plot(dates, posts, label='post count')
        plt.plot(dates, comments, label='comments analisys')
        plt.legend()
        plt.title('User: ' + user)
        plt.show()
    elif command == '-help' or command == '-?':
        pass
    else:
        print('[!] \'' + command + '\' is unknown argument.')


if __name__ == '__main__':
    main()
