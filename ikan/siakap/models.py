from django.db import models

class Project(models.Model):
    name = models.CharField(max_length=80)
    description = models.CharField(max_length=255)

class Station(models.Model):
    project = models.ForeignKey(to=Project, related_name="stations", on_delete=models.CASCADE)
    name = models.CharField(max_length=80)
    description = models.CharField(max_length=255)

class Failcode(models.Model):
    station = models.ForeignKey(to=Station, related_name="failcodes", on_delete=models.CASCADE)
    failcodeID = models.CharField(max_length=10)
    description = models.CharField(max_length=255)