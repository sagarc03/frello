"""Frello models"""
from django.contrib.auth import get_user_model
from django.db import models


class Project(models.Model):
    """
    Frello Project
    """

    name = models.CharField(verbose_name="Project name", max_length=150)
    description = models.TextField(
        verbose_name="Project description", default=""
    )
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    contributors = models.ManyToManyField(
        get_user_model(), related_name="project_contributors"
    )

    class Meta:
        unique_together = (
            "name",
            "owner",
        )


class Issue(models.Model):
    """
    Project Issue
    """

    class Status(models.TextChoices):
        """
        Status of each issue
        """

        OPENED = "OP", "opened"
        REOPENED = "RO", "reopened"
        CLOSED = "CL", "closed"

    issue_number = models.IntegerField()
    created_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=2, choices=Status.choices, default=Status.OPENED
    )
    title = models.CharField(max_length=150)
    description = models.TextField()
    is_delete = models.BooleanField(default=False)
    assigned_to = models.ForeignKey(
        get_user_model(),
        on_delete=models.DO_NOTHING,
        null=True,
        related_name="issue_assigned_to",
    )
