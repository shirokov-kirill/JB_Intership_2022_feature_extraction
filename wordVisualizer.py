import nltk
from nltk.probability import FreqDist
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt

class WordVisualizer:

    def __init__(self, data):
        self._data = data
        self._percentage = 0

    def visualize(self, percent):
        fig = plt.figure()
        counter = Counter(self._data)
        fdist = FreqDist(dict(counter))
        fdist.plot(round(len(dict(counter)) * percent), cumulative=False)
        plt.show()
        fig.savefig('freqDist.png', bbox_inches="tight")
        data_matplotlib = " ".join(self._data)
        word_cloud = WordCloud().generate(data_matplotlib)
        plt.figure()
        plt.imshow(word_cloud, interpolation='bilinear')
        plt.axis("off")
        plt.savefig('frequency_count.png')
