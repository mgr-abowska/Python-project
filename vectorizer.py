import pandas
import re
from sklearn.feature_extraction.text import CountVectorizer


def words_and_emoticons(text):
    emoticons = re.findall('[\u263a-\U0001f645]', text)
    for e in emoticons:
        yield e
    words = re.findall('\w{1,}', text)
    for w in words:
        yield w


vectorizer = CountVectorizer(analyzer=words_and_emoticons, binary=False)


df = pandas.read_csv('comments.csv',
            sep = ';',
            header=0,
            names=['user', 'comment'],
            error_bad_lines=False)

#dobry format
comments=[]
c=('Sama s\u0142odycz pani Magdo\ud83c\udf37\ud83c\udf37\ud83c\udf37\ud83d\ude42\ud83c\udf52\ud83c\udf52')
comments.append(c)

vectorizer.fit(comments)
print('ok (unicode):')
print(comments)
print(vectorizer.vocabulary_)



#taki sam ale text jest raw
comments=[]
c=(r'Sama s\u0142odycz pani Magdo\ud83c\udf37\ud83c\udf37\ud83c\udf37\ud83d\ude42\ud83c\udf52\ud83c\udf52')
comments.append(c)

vectorizer.fit(comments)
print('nie ok (raw):')
print(comments)
print(vectorizer.vocabulary_)



#zły format
comments=[]
c=df.iloc[10]['comment']
comments.append(c)

vectorizer.fit(comments)
print('nie ok (zapisany w csv):')
print(comments)
print(vectorizer.vocabulary_)



