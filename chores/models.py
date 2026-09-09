from django.db import models


class Member(models.Model):
    """A person in the household who chores can be assigned to."""

    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
