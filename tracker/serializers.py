from rest_framework import serializers

from .models import Objective, TimeEntry


class ObjectiveSerializer(serializers.ModelSerializer):
    lookup_field = "objective"

    class Meta:
        model = Objective
        fields = ("id", "name", "description", "target", "date_created", "total_effort", "progression",)
        read_only_fields = ("date_created", "total_effort", "progression",)


class TimeEntrySerializer(serializers.ModelSerializer):
    lookup_field = "entry"

    class Meta:
        model = TimeEntry
        fields = ("id", "user", "objective", "explanation", "effort", "submitter", "date_created",)
        read_only_fields = ("user", "date_created",)
