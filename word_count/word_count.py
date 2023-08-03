
class WordCounter:

    def __init__(self, text: str):
        self.text = text
    
    def count(self):
        """Count number of words in input text."""

        return len(self.text.split())
