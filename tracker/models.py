from django.db import models


class Objective(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    target = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    date_created = models.DateTimeField()

    def is_reached(self):
        return sum([entry.effort for entry in self.timeentry_set.all()]) >= self.target
    is_reached.admin_order_field = "goal"
    is_reached.boolean = True
    is_reached.short_description = "Reached"

    def __str__(self):
        return self.name


class TimeEntry(models.Model):
    objective = models.ForeignKey(Objective, on_delete=models.CASCADE)
    explanation = models.TextField()
    effort = models.DecimalField(max_digits=6, decimal_places=2)
    date_created = models.DateTimeField()

    def __str__(self):
        return self.explanation
