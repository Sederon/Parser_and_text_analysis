from nrclex import NRCLex
from nltk.sentiment import SentimentIntensityAnalyzer

class EmotionalAnalysis:
    def __init__(self, tokens, text):
        self.tokens = tokens
        self.text = text


    def emotions(self):
        lexicon = NRCLex(self.text)

        emotion_distribution = lexicon.raw_emotion_scores
        top_emotion_score = 0
        top_emotion = ''
        sum = 0
        for emot in emotion_distribution:
            if emot == "anticip" or emot == "positive" or emot == "negative":
                continue
            sum += emotion_distribution[emot]
        for emot in emotion_distribution:
            if emot == "anticip" or emot == "positive" or emot == "negative":
                continue
            freq = emotion_distribution[emot]/sum
            if freq > top_emotion_score:
                top_emotion_score = freq
                top_emotion = emot

        print(top_emotion_score)
        return emotion_distribution, [top_emotion, top_emotion_score]

    def sentiment(self):
        sia = SentimentIntensityAnalyzer()
        sentiment_scores = [sia.polarity_scores(sentence) for sentence in self.tokens]
        # Calculate average sentiment score
        av_pos = sum([score['pos'] for score in sentiment_scores]) / len(sentiment_scores)
        av_neg = sum([score['neg'] for score in sentiment_scores]) / len(sentiment_scores)
        av_neu = sum([score['neu'] for score in sentiment_scores]) / len(sentiment_scores)

        return av_pos, av_neg, av_neu
