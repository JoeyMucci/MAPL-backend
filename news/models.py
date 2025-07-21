from django.db import models

class Reporter(models.Model):
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=256)

    def __str__(self):
        return self.name

class Report(models.Model):
    author = models.ForeignKey(Reporter, on_delete=models.CASCADE, related_name='reports')
    year = models.IntegerField()
    month = models.IntegerField()
    day = models.IntegerField()
    content = models.TextField()
    title = models.CharField(max_length=1024)

    def __str__(self):
        return f"{self.month}/{self.day}/{self.year}: {self.title}"
