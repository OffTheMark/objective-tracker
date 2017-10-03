from datetime import datetime
from django.db import models

from django.contrib.auth.models import User


class Objective(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    target = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    date_created = models.DateTimeField(default=datetime.now)

    def total_effort(self):
        return sum([entry.effort for entry in self.timeentry_set.all()])

    def progression(self):
        return (self.total_effort() / self.target) * 100

    def is_reached(self):
        return self.total_effort() >= self.target
    is_reached.admin_order_field = "goal"
    is_reached.boolean = True
    is_reached.short_description = "Reached"

    def __str__(self):
        return self.name


class TimeEntry(models.Model):
    user = models.ForeignKey(User, null=True)
    objective = models.ForeignKey(Objective, on_delete=models.CASCADE)
    explanation = models.TextField()
    effort = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    date_created = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.explanation

    class Meta:
        verbose_name_plural = "Time entries"
