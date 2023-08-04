from django.db import models


class WordCount(models.Model):
    input_text = models.TextField()
    result = models.CharField(max_length=100, blank=True, default='')

    def __str__(self):
        return self.input_text
