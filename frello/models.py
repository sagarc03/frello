"""Frello models"""
from django.contrib.auth import get_user_model
from django.db import models


class Project(models.Model):
    """
    Project
    """

    name = models.CharField(verbose_name="Project name", max_length=150)
    description = models.TextField(verbose_name="Project description")
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    contributors = models.ManyToManyField(
        get_user_model(), related_name="project_contributors"
    )


class Issue(models.Model):
    class Status(models.TextChoices):
        OPENED = "OP", "opened"
        REOPENED = "RO", "reopened"
        CLOSED = "CL", "closed"

    issue_number = models.IntegerField()
    create_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=2, choices=Status.choices, default=Status.OPENED
    )
    is_delete = models.BooleanField(default=False)