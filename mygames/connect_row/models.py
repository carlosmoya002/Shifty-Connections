from django.db import models
import random

class Vocabulary(models.Model):
    word = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = "Vocabulary"

    def __str__(self):
        return self.word

class Connection(models.Model):
    word1 = models.ForeignKey(Vocabulary, related_name='word1', on_delete=models.CASCADE)
    word2 = models.ForeignKey(Vocabulary, related_name='word2', on_delete=models.CASCADE)
    word3 = models.ForeignKey(Vocabulary, related_name='word3', on_delete=models.CASCADE)
    word4 = models.ForeignKey(Vocabulary, related_name='word4', on_delete=models.CASCADE)
    description = models.TextField()
    difficulty = models.IntegerField()

    def __str__(self):
        return f'{self.word1}, {self.word2}, {self.word3}, {self.word4} - Difficulty: {self.difficulty}'

class Game(models.Model):
    connection1 = models.ForeignKey(Connection, related_name='connection1', on_delete=models.CASCADE)
    connection2 = models.ForeignKey(Connection, related_name='connection2', on_delete=models.CASCADE)
    connection3 = models.ForeignKey(Connection, related_name='connection3', on_delete=models.CASCADE)
    connection4 = models.ForeignKey(Connection, related_name='connection4', on_delete=models.CASCADE)
    difficulty = models.IntegerField()  # Difficulty of the entire game
    created_at = models.DateTimeField(auto_now_add=True)
    current_state = models.JSONField(default=list, blank=True)  # Optional current state field
    locked_rows_count = models.IntegerField(default=0)  # Track the number of locked rows

    def __str__(self):
        return f'Game ID: {self.id} - Difficulty: {self.difficulty}'

    def save(self, *args, **kwargs):
        # Auto-fill current_state with shuffled words from connections if not provided
        if not self.current_state:
            all_words = [
                self.connection1.word1.word, self.connection1.word2.word, self.connection1.word3.word, self.connection1.word4.word,
                self.connection2.word1.word, self.connection2.word2.word, self.connection2.word3.word, self.connection2.word4.word,
                self.connection3.word1.word, self.connection3.word2.word, self.connection3.word3.word, self.connection3.word4.word,
                self.connection4.word1.word, self.connection4.word2.word, self.connection4.word3.word, self.connection4.word4.word,
            ]
            random.shuffle(all_words)
            # Assuming a 4x4 matrix, fill in the current_state
            self.current_state = [all_words[i:i + 4] for i in range(0, len(all_words), 4)]
        
        super(Game, self).save(*args, **kwargs)
