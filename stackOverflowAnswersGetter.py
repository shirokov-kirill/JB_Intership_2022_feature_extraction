import requests
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re

#nltk.download('punkt')
#nltk.download('stopwords')
#nltk.download('averaged_perceptron_tagger')
stop_words = set(stopwords.words('english'))
CODE_RE = re.compile(r'<code>[^>]+</code>')
TAG_RE = re.compile(r'<[^>]+>')
forbiden_parts_of_speech = ['EX', 'PRP', 'TO', 'VBZ', 'VBP', 'VBN', 'VBG', 'VBD', 'VB', 'CD'] #modifiable

class StackOverflowAnswersGetter:

    def __init__(self):
        self._answers = []
        self._words = []

    @property
    def words(self):
        return self._words

    def formatWords(self):
        sentences = []
        bold_sentences = []
        self._words = []
        for ans in self._answers:
            sentences.extend(nltk.sent_tokenize(ans['body'],'english'))
        for sent in sentences:
            appending = re.sub('\W+', ' ', TAG_RE.sub('', CODE_RE.sub('', sent)))
            bold_sentences.append(appending)
        for bold_sent in bold_sentences:
            word_tokens = nltk.word_tokenize(bold_sent)
            filtered_sentence = [w for w in word_tokens if not w in stop_words]
            filtered_sentence = [w[0] for w in nltk.pos_tag(filtered_sentence) if not w[1] in forbiden_parts_of_speech]
            self._words.extend(filtered_sentence)

    def getStackOverflowAnswers(self):
        i = 1
        response = requests.get('https://api.stackexchange.com/2.3/answers',
                                params={
                                    'page': f'{i}',
                                    'pagesize': '100',
                                    'fromdate': '1629158400',
                                    'order': 'desc',
                                    'sort': 'creation',
                                    'site': 'stackoverflow',
                                    'filter': '!-)QWsboN0-4y'
                                })
        response_json = response.json()
        self._answers.extend(response_json['items'])
        while response_json['has_more']:
            i += 1
            response = requests.get('https://api.stackexchange.com/2.3/answers',
                                    params={
                                        'page': f'{i}',
                                        'pagesize': '100',
                                        'fromdate': '1629158400',
                                        'order': 'desc',
                                        'sort': 'creation',
                                        'site': 'stackoverflow',
                                        'filter': '!-)QWsboN0-4y'
                                    })
            response_json = response.json()
            self._answers.extend(response_json['items'])
        return
