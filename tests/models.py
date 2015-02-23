from django.db import models


class ExtraModel(models.Model):
    content = models.CharField(max_length=256)


class FirstModel(models.Model):
    content = models.CharField(max_length=256)
    extra = models.ForeignKey('ExtraModel')


class SecondModel(models.Model):
    content = models.CharField(max_length=256)
    extra = models.ForeignKey('ExtraModel')
    first = models.ForeignKey('FirstModel')


class ThirdModel(models.Model):
    content = models.CharField(max_length=256)
    extra = models.ForeignKey('ExtraModel')
    second = models.ForeignKey('SecondModel')
