import json
import jwt

from django.http import JsonResopnse
from django.views import View

from .models import UserWatched 
from movie.models import Movie, Series
from user.models import SubUser

# Create your views here.

class AddUserWatchView(View):
    @jwt_utils.token
    def post(self, request):
        try:
            user = request.user

            data = json.loads(request.body)
            category = data['category']
            if category == 'movie':
                UserWatched.objects.create(
                    subuser=user,
                    movie=Movie.objects.get(id=data['id'])
                )
                return JsonResponse({'message': 'SAVED'}, status=201)
            
            UserWatched.objects.craete(
                subuser=user,
                series=SeriesVideo.objects.get(id=data['id'])
            )
            return JsonResponse({'message': 'SAVED'}, status=201)

        except KeyError as e:
            return JsonResopnse({'message': f'KEY_ERROR: {e}'}, status=400)
        except ValueError as e:
            return JsonResopnse({'message': f'VALUE_ERROR: {e}'}, status=400)


class ShowUserWatchedView(View):
    @jwt_utils.token
    def get(self, request):
        user = request.user

        histories = UserWatched.select_related(
            'movie',
            'series'
        ).objects.filter(
            subuser=user
        ).order_by(
            '-registered_at'
        )
        
        showing_lst = []
        series_lst = []
        while len(showing_lst) < 10:
            for history in histories:
                if not hasattr(history, 'series'):
                    showing_lst.append(history.movie)
                else:
                    if history.series.id not in series_lst:
                        series_lst.append(history.series.id)
                        showing_lst.append(history.series)

        return JsonResponse(
            {
                'history':[
                    {
                        'category':(
                            'movie' 
                            if not hasattr(history, 'series')
                            else 'series'
                        ),
                        'id': history.id,
                        'poster': history.poster1
                    } for history in showing_lst
                ]
            }
        )
