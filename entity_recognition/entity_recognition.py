import random


class EntityRecognizer:

    def __init__(self, text: str):
        self.text = text

    def get_entities(self):
        """Find entities in input text."""

        words = self.text.split()
        entities = []
        for word in words:
            if word[0].isupper():  # Let's just say any uppercase word is an entity
                entities.append(word)
        if entities == []:  # If we didn't find anything, pick a random sample
            entities = random.sample(words, random.randint(1, len(words)))
        return entities
