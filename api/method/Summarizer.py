from collections import defaultdict
from string import punctuation
from heapq import nlargest
import os

class FrequencySummarizer:
    def __init__(self,meeting_sentence, min_cut=0.1, max_cut=0.9):
        """
         Initilize the text summarizer.
         Words that have a frequency term lower than min_cut
         or higer than max_cut will be ignored.
        """
        self._min_cut = min_cut
        self._max_cut = max_cut
        self._stopwords = None
        self._meeting_sentence = meeting_sentence
        self._url_word_segmentation = 'https://api.aiforthai.in.th/lextoplus'
        self._url_word_similarity = "https://api.aiforthai.in.th/thaiwordsim"
        self._headers = {'Apikey':"jIu8xU0JhX9ZYO94VzvCCLooNQrjMPHH"}

    def construct_stopword(self):
        punctuation_list = []
        stop_word_list = []
        with open(os.path.dirname(os.path.realpath(__file__))+'\punctuation.txt','r',encoding='utf-8') as punctuation_file:
            for row in punctuation_file:
                row = row.strip()
                punctuation_list.append(row)
        with open(os.path.dirname(os.path.realpath(__file__))+'\stopword.txt','r',encoding='utf-8') as stopword_file:
            for row in stopword_file:
                row = row.strip()
                stop_word_list.append(row)
        self._stopwords = set(punctuation_list+stop_word_list+list(punctuation))

    def _compute_frequencies(self, word_sent):
        """
          Compute the frequency of each of word.
          Input:
           word_sent, a list of sentences already tokenized.
          Output:
           freq, a dictionary where freq[w] is the frequency of w.
        """

        #print('_compute_frequencies : ', word_sent)
        self.construct_stopword()
        freq = defaultdict(int)
        for s in word_sent:
          for word in s:
            #print('word in list : ' ,word)
            if word not in self._stopwords:
              freq[word] += 1

        #print(freq)
        # frequencies normalization and fitering
        m = float(max(freq.values()))
        for w in list(freq):
          freq[w] = freq[w]/m
          if freq[w] >= self._max_cut or freq[w] <= self._min_cut:
            del freq[w]
        return freq

    def _find_word_similarity(self, word_list):

        self.construct_stopword()

        word_sim_list = []
        for sentence in word_list:
          for word in sentence:
            if word not in self._stopwords:
              #print('word in list for find simalarity : ' ,word)
              import requests

              params = {'word':word,'model':'thwiki','numword':'2'}

              response = requests.get(self._url_word_similarity , headers=self._headers, params=params)

              word_sim = []
              for w in response.json()['words']:
                word_sim.append(w['word'])

          sentence = sentence + word_sim
          word_sim_list.append(sentence)

        return word_sim_list

    def summarize(self, n):
        """
          Return a list of n sentences
          which represent the summary of text.
        """
        # sents = []
        # with open('output.txt','r',encoding='utf-8')as output:
        #     for row in output:
        #         row = row.strip()
        #         sents.append(row)
        # # sents = sent_tokenize(text)
        # assert n <= len(sents)

        # meeting_content = []
        # for i in self._meeting_sentence:
        #    meeting_content.append(i['string_data'])

        # print( meeting_content)

        # ------------- รับการตัดคำจาก speech to text ---------------------

        import requests

        meeting_content_word = []
        for text in self._meeting_sentence:
          params = {'text':text,'norm':'1'}

          response = requests.get(self._url_word_segmentation, params=params, headers=self._headers)

          meeting_content_word.append(response.json()['tokens'])

        #print(meeting_content_word)
        # ---------------------------------------------------------------

        # ------ Word Similarity -----
        meeting_word_sim = self._find_word_similarity(meeting_content_word)

        # ---------------------------------------------------------------
        self._freq = self._compute_frequencies(meeting_word_sim)
        #print(self._freq)

        ranking = defaultdict(int)
        for i,sent in enumerate(meeting_word_sim):
          for w in sent:
            if w in self._freq:
              ranking[i] += self._freq[w]
        sents_idx = self._rank(ranking, n)
        return [self._meeting_sentence[j] for j in sents_idx]

    def _rank(self, ranking, n):
        """ return the first n sentences with highest ranking """
        return nlargest(n, ranking, key=ranking.get)
