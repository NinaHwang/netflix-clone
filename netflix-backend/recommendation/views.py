import json

from django.http import JsonResponse
from django.views import View

from movie.models import (
    Movie,
    Series,
    Tag,
    MovieTag,
    SeriesTag
)

# Create your views here.

class MostPopularView(View):
    @jwt_utils.token
    def get(self, request):
        top_ten = analysis.top_ten_video()

        li = []

        for video in top_ten:
            if video[0] == 'm':
                v = Movie.objects.get(id=int(video[1:]))
                category = 'movie'
            else:
                v = Series.objects.get(id=int(video[1:]))
                categor = 'series'

            li.append(
                {
                    'category': category,
                    'id': v.id,
                    'poster': v.poster1
                }
            )

        return JsonResopnse({'top_ten':li}, status=200)

