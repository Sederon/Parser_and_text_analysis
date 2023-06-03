import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from string import punctuation

from sklearn.feature_extraction.text import TfidfVectorizer

from tools.Summarizator import Summarizator
from tools.Emotions import EmotionalAnalysis

# nltk.download('vader_lexicon')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('punkt')
# nltk.download('stopwords')


class TextProcessing:
    def __init__(self, text, sum_method, language: str = 'english'):
        self.text = text
        self.language = language
        self.keywords = []
        self.tagged_sentences = []

        self.sentiment = []
        self.emotions = []
        self.keywords_number = 5
        self.sentence_num = 1

        smrztn = Summarizator(text, sum_method, language)
        self.summary = smrztn.summarize_text(self.sentence_num)

        self.analyse_text()

    # Basic analysis
    def analyse_text(self):
        text = self.text_cleaner(self.text)
        # Tokenization
        tokens = word_tokenize(text)

        # Stopword and punctuation removal
        stop_words = set(stopwords.words(self.language))
        filtered_tokens = [token for token in tokens if token.lower() not in stop_words and token not in punctuation]

        # Keyword extraction
        freq_dist = nltk.FreqDist(filtered_tokens)
        self.keywords = freq_dist.most_common(self.keywords_number)  # Get the top n most frequent words as keywords

        # Sentiment analysis
        emot_analyse = EmotionalAnalysis(filtered_tokens, text)
        self.emotions = emot_analyse.emotions()
        self.sentiment = emot_analyse.sentiment()

        # Part-of-speech tagging
        # self.tagged_sentences = [nltk.pos_tag(nltk.word_tokenize(sentence)) for sentence in filtered_tokens]

    def tf_idf(self):
        vectorizer = TfidfVectorizer(stop_words=self.language)
        tf_idf = vectorizer.fit_transform(sent_tokenize(self.text))
        print("Token's used as Features ")
        print(vectorizer.get_feature_names_out(), "\n")
        print("Size of the array")
        print(tf_idf.shape, "\n")
        print("TF-IDF Matrix\n")
        print(tf_idf.toarray())

    @staticmethod
    def text_cleaner(text_in):
        # Cleaning text
        text = text_in
        text = re.sub(r"""['’"`�]""", '', text)
        text = re.sub(r"""([0-9])([\u0400-\u04FF]|[A-z])""", r"\1 \2", text)
        text = re.sub(r"""([\u0400-\u04FF]|[A-z])([0-9])""", r"\1 \2", text)
        text = re.sub(r"""[\-.,:+*/_]""", ' ', text)
        return text

    def print_result(self):
        str_arr = []
        str_arr.append("Keywords:")
        for keyword, frequency in self.keywords:
            str_arr.append(f"\n{keyword}-{frequency}")

        str_arr.append("\nPositive: {0: 0.000}, Negative: {1: 0.000}, Neutral:{2: 0.000}\n".format(self.sentiment[0],
                                                                                      self.sentiment[1],
                                                                                      self.sentiment[2]))
        # str_arr.append(f"Pos:{self.emotions[2][0]}, Neg:{self.emotions[2][1]}\n")

        for item in self.emotions[0]:
            if item == "anticip" or item == "positive" or item == "negative":
                continue
            str_arr.append("{0}: {1}; ".format(item, self.emotions[0][item]))

        str_arr.append("\nTop emot: {0}: {1}\n".format(self.emotions[1][0], self.emotions[1][1]))

        str_arr.append(f"\nSummary of the text: {self.summary[0]}")

        # print("Part-of-Speech Tagging:")
        # for i, tagged_sentence in enumerate(self.tagged_sentences):
        #     print("Sentence", i + 1)
        #     print(tagged_sentence)
        #     print()

        return "".join(str_arr)



