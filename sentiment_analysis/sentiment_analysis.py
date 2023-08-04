import random


class SentimentAnalyzer:

    def __init__(self, text: str):
        self.text = text
        self.sentiments = ["Happy", "Sad", "Angry", "Excited", "Worried", "Confused"]

    def analyze(self):
        """Return computed sentiment of input text (use random choice of sentiment to mock out function)."""

        return random.choice(self.sentiments)
