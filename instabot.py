import time

from model import CommentModel
from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import sys
import random
import datetime
import shelve


def save(f):
    def persist(self):
        f(self)
        profile_statistics = self.analyze_profile(self.username)
        db = shelve.open('statistics')
        db[str(datetime.datetime.now()) + '||' + self.username] = profile_statistics
        db.close()

    return persist


class InstaBot:
    """
    A class used to
    - navigate
    - scrap information
    - gather data
    - calculate decisions based on other classes
    from www.instagram.com
    ...

    """

    def __init__(self, **kwargs):
        self.__dict__ = kwargs
        self.driver = webdriver.Chrome(kwargs["driver_path"])
        self.model = CommentModel()
        self.model.load()

    """
    Method used to login to our profile [self.username, self.password] (using xPATH) 
    """

    def login(self):
        print('[->] logging in...')
        self.driver.get(self.base_url)
        time.sleep(5)
        self.driver.find_element_by_xpath("//input[@name=\"username\"]").send_keys(self.username)
        self.driver.find_element_by_xpath("//input[@name='password']").send_keys(self.password)
        self.driver.find_element_by_xpath('//button[@type= "submit"]').click()
        print('[->] logged in!')

    """
    Method used to logout from our profile (using xPATH) 
    """

    def logout(self):
        self.go_to_user(self.username)
        self.driver.find_element_by_xpath(
            '//*[@id="react-root"]/section/main/div/header/section/div[1]/div/button').click()
        time.sleep(1)
        self.driver.find_element_by_xpath('//button[contains(text(), "Log Out")]').click()
        time.sleep(1)
        try:
            self.driver.find_element_by_xpath('//button[contains(text(), "Log Out")]').click()
        except Exception:
            pass
        time.sleep(3)

    """
    Method used to kill driver session
    """

    def end_session(self):
        self.driver.close()

    """
                                [---> WEBSITE NAVIGATION  <---] 
    """

    """
    Main method of the class: navigation
    """

    @save
    def start_session(self):

        self.login()
        time.sleep(5)

        likes_to_go = self.likes_in_session
        follows_to_go = self.follows_in_session

        iteration = 1
        while max(likes_to_go, follows_to_go) > 0:

            print('\n[ --- ITERATION no. ' + str(iteration) + ' --- ]')
            pic_hrefs = self.prepare_data(max(likes_to_go, follows_to_go))
            for pic in pic_hrefs:

                self.driver.get(pic)
                profile_to_analyze = self.driver.find_element_by_xpath \
                    ('//*[@id="react-root"]/section/main/div/div[1]/article/header/div[2]/div[1]/div/a').text
                profile_rating = self.calculate_score(self.analyze_profile(profile_to_analyze))
                self.driver.back()

                print('[->] analysis of ' + profile_to_analyze + ' finished, score = ' + str(profile_rating))

                if profile_rating > self.min_rating or max(likes_to_go, follows_to_go) < 10:

                    if likes_to_go > 0:
                        time.sleep(2)
                        self.driver.find_element_by_xpath \
                            ('//*[@id="react-root"]/section/main/div/div[1]/article/div[2]/section[1]/span[1]/button') \
                            .click()
                        likes_to_go -= 1

                    time.sleep(2)

                    if follows_to_go > 0:
                        self.driver.find_element_by_xpath \
                            ('//*[@id="react-root"]/section/main/div/div[1]/article/header/div[2]/div[1]/div[2]/button') \
                            .click()
                        follows_to_go -= 1

                    delay = random.randint(self.min_separation_time, self.max_separation_time)
                    print('[:/] waiting delay: ' + str("{:.2f}".format(delay / 60)) + ' [min].')
                    time.sleep(delay)
                else:
                    print('[!] score too low - rejecting profile.')
        iteration += 1

    """
    Method used to enter profile of chosen user 
    """

    def go_to_user(self, username):
        if self.driver.current_url == self.base_url + '/' + username + '/':
            return

        self.driver.get(self.base_url + '/' + username + '/')

    """
    Method used to prepare data for session 
    (finds hrefs to pictures) 
    """

    def prepare_data(self, target_likes):

        print('[->] gathering information, traget: ' + str(target_likes) + ' posts.')

        result_hrefs = []
        equal_post_split = max(1, int(target_likes / (len(self.hashtags))))

        # hashtags
        for hashtag in self.hashtags:

            pic_hrefs = []
            self.driver.get("https://www.instagram.com/explore/tags/" + hashtag + "/")
            time.sleep(2)

            for i in range(1, max(2, int(equal_post_split / 9))):
                try:
                    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(2)

                    hrefs_in_view = self.driver.find_elements_by_tag_name('a')
                    hrefs_in_view = [elem.get_attribute('href') for elem in hrefs_in_view
                                     if '.com/p/' in elem.get_attribute('href')]
                    [pic_hrefs.append(href) for href in hrefs_in_view if href not in pic_hrefs]

                except:
                    continue

            for i in range(0, (len(pic_hrefs) - equal_post_split)):
                pic_hrefs.remove(random.choice(pic_hrefs))

            result_hrefs.extend(pic_hrefs)

        print('[->] gathering finished, found: ' + str(len(result_hrefs)) + ' posts.')
        return result_hrefs

    """
                                [---> PROFILE ANALYSIS  <---] 
    """

    """
    Method used to calculate profile analysis score
    """
    @staticmethod
    def calculate_score(data):
        result = max(1, min(0, data['followers_count']/data['following_count'])) * 0.5 + data['comments_analysis'] * 0.5
        print('final score: ' + str(result))
        return result

    """
    Method used to gather data for score calculation 
    """

    def analyze_profile(self, username):

        self.go_to_user(username)
        time.sleep(3)

        print('\n[->] analysis of ' + username)
        average_post_likes = 0
        comment_analysis = 0
        time.sleep(2)

        pic_hrefs = []
        for i in range(1, 2):
            try:
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)

                hrefs_in_view = self.driver.find_elements_by_tag_name('a')
                hrefs_in_view = [elem.get_attribute('href') for elem in hrefs_in_view
                                 if '.com/p/' in elem.get_attribute('href')]
                [pic_hrefs.append(href) for href in hrefs_in_view if href not in pic_hrefs]

            except:
                continue

        each_post_likes = list()
        each_post_comments = list()

        if len(pic_hrefs) != 0:

            for index in range(0, min(int(0.3 * len(pic_hrefs)), 20)):
                picture_url = pic_hrefs[index]
                self.driver.get(picture_url)
                time.sleep(3)
                try:
                    str_post_likes = self.driver.find_element_by_xpath \
                        ('//*[@id="react-root"]/section/main/div/div[1]/article/div['
                         '2]/section[2]/div/div/button/span').text
                except:
                    str_post_likes = '1'
                    pass

                each_post_likes.append(int("".join(str_post_likes.split())))
                each_post_comments.extend(self.get_comments())

            if len(each_post_likes) != 0:
                average_post_likes = sum(each_post_likes) / len(each_post_likes)
            else:
                average_post_likes = 0

            if len(each_post_comments) != 0:
                model_result = self.model.predict(each_post_comments)
                comment_analysis = sum(model_result) / len(model_result)
            else:
                comment_analysis = 0

        post_count = int("".join(self.get_posts_count(username).split()))
        followers_count = int("".join(self.get_followers_count(username).split()))
        following_count = int("".join(self.get_following_count(username).split()))

        print('f/f ratio: ' + str(followers_count/following_count))
        print('average post likes: ' + str(average_post_likes))
        print('comment score: ' + str(comment_analysis))

        return {'followers_count': followers_count,
                'following_count': following_count,
                'post_count': post_count,
                'average_post_likes': average_post_likes,
                'comments_analysis': comment_analysis}

    """
    Method used to scrap comments from profile
    """

    def get_comments(self):

        try:
            page = requests.get(self.driver.current_url)
            soup = BeautifulSoup(page.content, 'html.parser')
            data = str(soup.find_all('script', type="text/javascript")[3])
            data = data[52:]
            data = data[data.find('"display_url":') + 15:]
            data = data[data.find('"edge_threaded_comments"'):]
            data = data[data.find('"edges"'):]

            comments = []
            while (True):
                s = data.find('"text":"')
                if s == -1:
                    break
                data = data[s + 8:]
                comment = data[:data.find('"')]
                i = -1
                for c in comment:
                    i += 1
                    if c == '\\':
                        try:
                            comment = comment.replace(comment[i:i + 6], chr(int(comment[i + 2:i + 6], 16)), 1)
                            i -= 5
                        except ValueError:
                            pass
                comments.append(comment)
            return comments

        except:
            pass

    """
    Method used to get followers list 
    """

    def get_followers_list(self, username):

        self.go_to_user(username)
        time.sleep(2)

        self.driver.find_element_by_xpath('//a[@href= "/{}/followers/"]'.format(username)).click()
        time.sleep(2)

        scrollbox = self.driver.find_element_by_xpath('/html/body/div[4]/div/div[2]')
        last_height, curr_height = 0, 1

        while last_height != curr_height:
            last_height = curr_height
            time.sleep(1)
            curr_height = self.driver.execute_script("""arguments[0].scrollTo(0, arguments[0].scrollHeight);
              return arguments[0].scrollHeight;
              """, scrollbox)
            time.sleep(2)

        follower_links = scrollbox.find_elements_by_tag_name('a')
        followers_names = [name.text for name in follower_links]
        followers_names = [x for x in followers_names if x != '']

        try:
            self.driver.find_element_by_xpath(
                '/html/body/div[4]/div/div[1]/div/div[2]/button').click()
        except Exception:
            pass

        return followers_names

    """
    Method used to get followers count
    """

    def get_followers_count(self, username):
        self.go_to_user(username)
        time.sleep(2)
        return self.driver.find_element_by_xpath \
            ('//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a/span').text

    """
    Method used to get following list
    """

    def get_following_list(self, username):

        self.go_to_user(username)
        time.sleep(2)

        self.driver.find_element_by_xpath('//a[@href= "/{}/following/"]'.format(username)).click()
        time.sleep(2)

        scrollbox = self.driver.find_element_by_xpath('/html/body/div[4]/div/div[2]')
        last_height, curr_height = 0, 1
        while last_height != curr_height:
            last_height = curr_height
            time.sleep(1)
            curr_height = self.driver.execute_script("""arguments[0].scrollTo(0, arguments[0].scrollHeight);
            return arguments[0].scrollHeight;
            """, scrollbox)

            time.sleep(1)

        following_links = scrollbox.find_elements_by_tag_name('a')
        following_names = [name.text for name in following_links]
        following_names = [x for x in following_names if x != '']

        try:
            self.driver.find_element_by_xpath(
                '/html/body/div[4]/div/div[1]/div/div[2]/button').click()  # Click the [x] button for followers
        except Exception:
            pass

        return following_names

    """
    Method used to get following count 
    """

    def get_following_count(self, username):
        self.go_to_user(username)
        time.sleep(2)
        return self.driver.find_element_by_xpath \
            ('//*[@id="react-root"]/section/main/div/header/section/ul/li[3]/a/span').text

    """
    Method used to get posts count 
    """

    def get_posts_count(self, username):
        self.go_to_user(username)
        time.sleep(2)
        return self.driver.find_element_by_xpath \
            ('//*[@id="react-root"]/section/main/div/header/section/ul/li[1]/span/span').text
