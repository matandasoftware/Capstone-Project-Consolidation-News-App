from django.db import models

# Create your models here.
class Note(models.Model):
    ''' Model representing a sticky note
    Attributes:
        title (str): The note's title.
        content (str): The note's content.
        author (str): The note's author.
        created_at (datetime): The note's creation timestamp.
        updated_at (datetime): The note's last updated timestamp.
    '''

    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title