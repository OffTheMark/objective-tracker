from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from tracker.models import Objective, TimeEntry
from tracker.serializers import ObjectiveSerializer, TimeEntrySerializer


@api_view(["GET"])
def api_root(request, format=None):
    return Response({
        "objectives": reverse("tracker:api/objective-list", request=request, format=format),
        "entries": reverse("tracker:api/entry-list", request=request, format=format),
    })


class ObjectiveList(generics.ListAPIView):
    queryset = Objective.objects.all()
    serializer_class = ObjectiveSerializer


class ObjectiveDetail(generics.RetrieveAPIView):
    lookup_url_kwarg = "objective"
    queryset = Objective.objects.all()
    serializer_class = ObjectiveSerializer


class EntryList(generics.ListCreateAPIView):
    queryset = TimeEntry.objects.all()
    serializer_class = TimeEntrySerializer


class EntryDetail(generics.RetrieveAPIView):
    lookup_url_kwarg = "entry"
    queryset = TimeEntry.objects.all()
    serializer_class = TimeEntrySerializer


@api_view(["GET"])
def entry_list_by_objective(request, objective):
    if request.method == "GET":
        entries = TimeEntry.objects.filter(objective=objective)
        serializer = TimeEntrySerializer(entries, many=True)
        return Response(serializer.data)
