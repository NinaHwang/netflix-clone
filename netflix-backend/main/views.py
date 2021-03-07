from json
from jwt

from django.http import JsonResponse
from django.views import View

from movie.models import (
    Movie,
    Series,
    Tag
)

# Create your views here.

class RecommendListView(View):
    @jwt_utils.token
    def get(self, request):
        data = json.loads(request.body)

        # either movie or series
        category = data['category']
        tag = data['tag']

        if category == 'movie':
            targets = Movie.objects.filter(
                movietag_set_tag=tag
            )
            
            return JsonResponse(
                {
                    'movies': [
                        {
                            'movie_id': target.id,
                            'poster': target.poster
                        } for target in targets
                    ] 
                }, status=200
            )

        targets = Series.objects.filter(
            seriestag_set_tag=tag
        )

        return JsonResponse(
            {
                'series': [
                    {
                        'series_id': target.id,
                        'poster': target.poster
                    } for target in targets
                ]
            }, status=200
        )
