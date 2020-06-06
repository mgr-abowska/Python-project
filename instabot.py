from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import sys
import random
import time
import shelve

class InstaBot:
    def __init__(self,**kwargs):
        self.__dict__ = kwargs
        self.driver = webdriver.Chrome(kwargs["driver_path"])
        # ***

    """
    Kontrolki 
    """


    def login(self):
        print('[->] logging in...')
        self.driver.get(self.base_url)
        time.sleep(5)
        self.driver.find_element_by_xpath("//input[@name=\"username\"]").send_keys(self.username)
        self.driver.find_element_by_xpath("//input[@name='password']").send_keys(self.password)
        self.driver.find_element_by_xpath('//button[@type= "submit"]').click()
        print('[->] logged in!')

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

    def end_seesion(self):
        self.driver.close()

    """
    NAV
    """
    @save
    def start_session(self):
        # -> database zapisz liste followersow/followujacych etc.
        # -> zapisz statystyki naszego profilu czy cos
        # -> zapisz co zostalo poliekowane (profil statsty etc.)

        self.login()
        time.sleep(5)

        likes_to_go = self.likes_in_session
        follows_to_go = self.follows_in_session

        iteration = 1
        while max(likes_to_go,follows_to_go) > 0:

            print('\n[ --- ITERATION no. ' + str(iteration) + ' --- ]')
            pic_hrefs = self.prepare_data(max(likes_to_go,follows_to_go))
            for pic in pic_hrefs:

                self.driver.get(pic)
                profile_to_analyze = self.driver.find_element_by_xpath\
                    ('//*[@id="react-root"]/section/main/div/div[1]/article/header/div[2]/div[1]/div/a').text
                profile_rating = self.analyze_profile(profile_to_analyze)
                self.driver.back()

                print('\n[->] analysis of ' + profile_to_analyze + ' finished, score = ' + str(profile_rating))

                if profile_rating > self.min_rating or max(likes_to_go + follows_to_go) < 10:

                    if likes_to_go > 0:
                        time.sleep(2)
                        self.driver.find_element_by_xpath\
                            ('//*[@id="react-root"]/section/main/div/div[1]/article/div[2]/section[1]/span[1]/button')\
                            .click()
                        likes_to_go -= 1

                    time.sleep(2)

                    if follows_to_go > 0:
                        self.driver.find_element_by_xpath\
                            ('//*[@id="react-root"]/section/main/div/div[1]/article/header/div[2]/div[1]/div[2]/button')\
                            .click()
                        follows_to_go -= 1

                    delay = random.randint(self.min_separation_time, self.max_separation_time)
                    print('[:/] waiting delay: ' + str("{:.2f}".format(delay / 60)) + ' [min].')
                    time.sleep(delay)
        iteration += 1



    def go_to_user(self, username):
        if self.driver.current_url == self.base_url + '/' + username + '/':
            return

        self.driver.get(self.base_url + '/' + username + '/')

    def prepare_data(self, target_likes):

        print('[->] gathering information, traget: ' + str(target_likes) + ' posts.')

        result_hrefs = []
        equal_post_split = max(1, int(target_likes/(len(self.hashtags))))

        #hashtags
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

                except Exception:
                    continue

            for i in range(0, (len(pic_hrefs) - equal_post_split)):
                pic_hrefs.remove(random.choice(pic_hrefs))

            result_hrefs.extend(pic_hrefs)

        print('[->] gathering finished, found: ' + str(len(result_hrefs)) + ' posts.')
        return result_hrefs

    """
    Analysis 
    """

    def analyze_profile(self, username):

        self.go_to_user(username)
        time.sleep(2)

        return 0.6

        try:
            followers_count = self.get_followers_count(username)
            following_count = self.get_following_count(username)
            post_count = int(self.get_posts_count(username))
            average_post_likes = 0
            time.sleep(2)
        except Exception:
            print('error')

        pic_hrefs = []
        for i in range(1, max(2, int(post_count/9))):
            try:
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)

                hrefs_in_view = self.driver.find_elements_by_tag_name('a')
                hrefs_in_view = [elem.get_attribute('href') for elem in hrefs_in_view
                                 if '.com/p/' in elem.get_attribute('href')]
                [pic_hrefs.append(href) for href in hrefs_in_view if href not in pic_hrefs]

                if len(pic_hrefs) >= self.analyze_post_max:
                    break

            except Exception:
                continue

        if len(pic_hrefs) != 0:

            #likes
            chosen_post_count = min(int(self.analyze_post_precentage * post_count), self.analyze_post_max)
            chosen_post_indexes = random.sample(
                range(post_count),
                chosen_post_count)

            each_post_likes = list()

            for index in chosen_post_indexes:
                picture_url = pic_hrefs[index]
                self.driver.get(picture_url)
                time.sleep(2)
                each_post_likes.append(int(self.driver.find_element_by_xpath\
                    ('//*[@id="react-root"]/section/main/div/div[1]/article/div[2]/section[2]/div/div/button/span').text))

                #comments
                print(self.get_comments())


            average_post_likes = len(each_post_likes)/chosen_post_count
            print(average_post_likes)

            self.profile_statistics={'followers_count':self.get_followers_count(username),
            'following_count':self.get_following_count(username),
            'post_count':int(self.get_posts_count(username)),
            'average_post_likes':0}

            return true


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

    def get_followers_count(self, username):
        self.go_to_user(username)
        time.sleep(2)
        return self.driver.find_element_by_xpath\
            ('//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a/span').text

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

            time.sleep(1) # todo make timeout self.

        following_links = scrollbox.find_elements_by_tag_name('a')
        following_names = [name.text for name in following_links]
        following_names = [x for x in following_names if x != '']

        try:
            self.driver.find_element_by_xpath(
                '/html/body/div[4]/div/div[1]/div/div[2]/button').click()  # Click the [x] button for followers
        except Exception:
            pass

        return following_names

    def get_following_count(self, username):
        self.go_to_user(username)
        time.sleep(2)
        return self.driver.find_element_by_xpath\
            ('//*[@id="react-root"]/section/main/div/header/section/ul/li[3]/a/span').text

    def get_posts_count(self, username):
        self.go_to_user(username)
        time.sleep(2)
        return self.driver.find_element_by_xpath\
            ('//*[@id="react-root"]/section/main/div/header/section/ul/li[1]/span/span').text

def save(f):
    def persist(self):
        self.analyze_profile(self.username)
        db = shelve.open('statistics')
        db[time.ctime()] = self.profile_statistics
        db.close()
        self.f()
    return persist



