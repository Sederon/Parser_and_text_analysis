
from nltk.tokenize import RegexpTokenizer
from nltk.cluster.util import cosine_distance
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize

from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.summarizers.luhn import LuhnSummarizer
import numpy as np


class Summarizator:
    def __init__(self, text, sum_method, language: str = 'english'):
        self.text = text
        self.sum_method = sum_method
        self.language = language

    # Summarization sentence
    def summarize_text(self, num_sentences):
            text = self.text
            summary = 0
            if self.sum_method == 0:
                summary = self.generate_summary(text, num_sentences)
            elif self.sum_method == 1:
                parser = PlaintextParser.from_string(text, Tokenizer(self.language))
                # Initialize the LexRank summarizer
                summarizer = LexRankSummarizer()
                # Generate the summary
                summary = summarizer(parser.document, num_sentences)
            elif self.sum_method == 2:
                parser = PlaintextParser.from_string(text, Tokenizer(self.language))
                # Initialize the LSA summarizer
                summarizer = LsaSummarizer()
                # Generate the summary
                summary = summarizer(parser.document, num_sentences)
            elif self.sum_method == 3:
                parser = PlaintextParser.from_string(text, Tokenizer(self.language))
                # Initialize the Luhn summarizer
                summarizer = LuhnSummarizer()
                # Generate the summary
                summary = summarizer(parser.document, num_sentences)
            return summary

    def sentence_similarity(self, sent1, sent2, stop_words=None):
            if stop_words is None:
                stop_words = []

            sent1 = [token.lower() for token in sent1 if token.lower() not in stop_words and len(token) > 1]
            sent2 = [token.lower() for token in sent2 if token.lower() not in stop_words and len(token) > 1]

            all_words = list(set(sent1 + sent2))

            vector1 = [0] * len(all_words)
            vector2 = [0] * len(all_words)

            # Build vectors
            for token in sent1:
                vector1[all_words.index(token)] += 1

            for token in sent2:
                vector2[all_words.index(token)] += 1

            return 1 - cosine_distance(vector1, vector2)

    def generate_summary(self, text, num_sentences=1):
            # Tokenize the text into sentences
            sentences = sent_tokenize(text)

            # Remove punctuation and tokenize each sentence
            tokenizer = RegexpTokenizer(r'\w+')
            sentences = [tokenizer.tokenize(sentence) for sentence in sentences]

            # Filter out stop words
            stop_words = set(stopwords.words(self.language))
            sentences = [[token.lower() for token in sentence if token.lower() not in stop_words] for sentence in
                         sentences]

            # Calculate sentence similarity matrix
            similarity_matrix = np.zeros((len(sentences), len(sentences)))
            for i in range(len(sentences)):
                for j in range(len(sentences)):
                    if i != j:
                        similarity_matrix[i][j] = self.sentence_similarity(sentences[i], sentences[j], stop_words)

            # Apply PageRank algorithm (TextRank)
            scores = self.pagerank(similarity_matrix)

            # Get the top-ranked sentences
            ranked_sentences = sorted(((scores[i], i) for i in range(len(sentences))), reverse=True)
            summary_sentences = [sentences[idx] for _, idx in ranked_sentences[:num_sentences]]

            # Concatenate the summary sentences into a single string
            summary = ' '.join([' '.join(sentence) for sentence in summary_sentences])

            return summary

    def pagerank(self, similarity_matrix, damping=0.85, max_iterations=100, epsilon=1e-4):
            scores = np.ones(len(similarity_matrix)) / len(similarity_matrix)

            for _ in range(max_iterations):
                prev_scores = np.copy(scores)

                for i in range(len(similarity_matrix)):
                    summation = np.sum(similarity_matrix[:, i] * scores)
                    scores[i] = (1 - damping) + damping * summation

                if np.sum(np.abs(scores - prev_scores)) < epsilon:
                    break

            return scores
