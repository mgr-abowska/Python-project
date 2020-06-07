import re
import pickle
import pandas
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression


def words_and_emoticons(text):
    """Word analyzer used in vectorizer"""
    emoticons = re.findall('[\u263a-\U0001f645]', text)
    for e in emoticons:
        yield e
    words = re.findall('\w{1,}', text)
    for w in words:
        yield w

def formated(raw):
    """Comment formater into a modifiable list"""
    comments=[]
    for i in range(len(raw)):
            comment = raw[i]
            comment = comment.lower()
            comment = comment.rstrip('\\') # remove '\' at the end
            comments.append(comment)
    return comments


class CommentModel:
    """
    A class used to represent model for analyzing comments

    ...

    Attributes
    ----------
    comments : list
        a formatted list of comments to work with
    results : list
        list of values {0,1} defining whether a comment counts as complement
    vectorizer : object
        used for vectorizing comments
    model : object
        logistic regression based on current comments and results
    """

    def __init__(self):
        self.comments = []
        self.results = []
        self.vectorizer = None
        self.model = None

    def read_csv_comments(self, file_csv='comments1.csv'):
        df = pandas.read_csv(file_csv,
                             sep=';',
                             header=0,
                             names=['user', 'comment'],
                             error_bad_lines=False)

        encoded = df['comment'].to_numpy()
        for i in range(len(encoded)):
            comment = encoded[i]
            comment = comment.lower()
            comment = comment.rstrip('\\')  # remove '\' at the end
            comment = comment.encode('utf-8')
            comment = comment.decode('unicode_escape')  # remove escape chars
            self.comments.append(comment)

    def read_txt_comments(self, file_txt='comments0.txt'):
        with open(file_txt) as f:
            for comment in f.read().splitlines():
                comment = comment.lower()
                comment = comment.rstrip('\\')
                comment = comment.encode('utf-8')
                comment = comment.decode('unicode_escape')
                self.comments.append(comment)

    def read_txt_results(self, file_txt='results0.txt'):
        with open(file_txt) as f:
            for value in f.read().splitlines():
                self.results.append(int(value))

    def build(self):
        """Creating model based on current comments and results"""
        self.vectorizer = CountVectorizer(analyzer=words_and_emoticons, binary=False)
        self.vectorizer.fit(self.comments)

        x_train = self.vectorizer.transform(self.comments)
        y_train = self.results

        self.model = LogisticRegression(solver='liblinear')
        self.model.fit(x_train, y_train)

    def save(self):
        with open('res/insta_model', 'wb+') as picklefile:
            pickle.dump(self.model, picklefile)

        with open('res/insta_vectorizer', 'wb+') as picklefile:
            pickle.dump(self.vectorizer, picklefile)

    def load(self, model='res/insta_model', vectorizer='res/insta_vectorizer'):
        with open(model, 'rb') as model:
            self.model = pickle.load(model)

        with open(vectorizer, 'rb') as vectorizer:
            self.vectorizer = pickle.load(vectorizer)

    def predict(self, test_comments):
        test_comments = formated(test_comments)
        x_test = self.vectorizer.transform(test_comments)
        predicted = self.model.predict(x_test)
        return predicted

    def show_score(self, test_comments, test_results):
        x_test = self.vectorizer.transform(test_comments)
        y_test = test_results
        score = self.model.score(x_test, y_test)
        print(f'score: {score}')

    def show_properties(self):
        print(self.vectorizer.vocabulary_)
        print('---')
        print(self.vectorizer.transform(self.comments).toarray())


def create():
    """Function just to create upgraded model"""
    model = CommentModel()
    model.read_txt_comments('res/comments0.txt')
    model.read_txt_results('res/results0.txt')
    model.read_txt_comments('res/comments1.txt')
    model.read_txt_results('res/results1.txt')
    model.read_txt_comments('res/comments2.txt')
    model.read_txt_results('res/results2.txt')
    model.read_txt_comments('res/comments3.txt')
    model.read_txt_results('res/results3.txt')

    model.build()
    model.save()
