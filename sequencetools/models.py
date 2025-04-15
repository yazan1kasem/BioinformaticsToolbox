from django.db import models

"""
Erstelle in der models.py Datei ein Modell namens SequenceSubmission mit folgenden Feldern:
text_input: Ein TextField für Texteingaben
file_upload: Ein FileField für Datei-Uploads
submission_date: Ein DateTimeField, das automatisch den Zeitpunkt des Uploads speichert
"""


# Create your models here.
class SequenceSubmission(models.Model):
    text_input = models.TextField()
    file_upload = models.FileField()
    submission_date = models.DateTimeField(auto_now_add=True)


class ORF:
    def __init__(self, dna_sequence: str, min_orf_length: int, both_strands: bool):
        self.dna_sequence = dna_sequence
        self.min_orf_length = min_orf_length
        self.both_strands = both_strands

