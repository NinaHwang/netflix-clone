import json

from django.http import JsonResponse
from django.views import View

from movie.models import (
    Movie,
    Series,
    Tag
)

# Create your views here.
