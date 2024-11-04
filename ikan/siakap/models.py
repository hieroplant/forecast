from django.db import models

class Project(models.Model):
    name = models.CharField(max_length=80)
    description = models.CharField(max_length=255)

class Station(models.Model):
    project = models.ForeignKey(to=Project, related_name="station", on_delete=models.CASCADE)
    name = models.CharField(max_length=80)
    description = models.CharField(max_length=255) 