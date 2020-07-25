from django.shortcuts import render, redirect
from .models import Movie
from django.views.generic import ListView, DetailView
from django.http import HttpResponse, JsonResponse, Http404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.contrib import messages
from .functions import is_similar
from functools import reduce
# Create your views here.


class MoiveListView(ListView):
    model = Movie
    template_name = 'movies/home.html'
    queryset = [movie for movie in model.objects.all()
                if movie.cover]
    context_object_name = 'movie_list'
    paginate_by = 60


class MovieDetailView(DetailView):
    model = Movie
    tempalte_name = 'movies/movie_detail.html'


def get_recommendation(request):
    user = request.user
    is_random = not (user.moviepreference.favorite_movie.all()
                     or user.friends_set.all())

    if is_random:
        movie_list = [
            movie for movie in Movie.objects.order_by('?') if movie.cover][:30]
    else:
        # the recommendation algorithm goes here
        neighbours = []
        friends = user.friends_set.first().movie_friends.all(
        ) if user.friends_set.first() else []
        strangers = [stranger for stranger in User.objects.all() if (
            stranger.id != user.id) and (stranger not in friends)]

        for friend in friends:
            neighbours.append(friend)

        for stranger in strangers:
            if is_similar(stranger, user):
                neighbours.append(stranger)

        movie_list = list(
            set(reduce(lambda x, y: x+y,
                       [list(neighbour.moviepreference.favorite_movie.all())for neighbour in neighbours]))
        )
        movie_list = [
            movie for movie in movie_list if movie not in user.moviepreference.favorite_movie.all()]
        if len(movie_list) >= 30:
            movie_list = movie_list[:30]
        else:
            rest = 30 - len(movie_list)
            rest_movies = [movie for movie in Movie.objects.order_by(
                '?') if movie not in movie_list][:rest]
            movie_list += rest_movies
    return render(request, 'movies/movie_rec.html', {'movie_list': movie_list, 'is_random': is_random})


def show_friends(request):
    curr_user = request.user
    all_user_list = list(User.objects.all())
    rec_friends = [user for user in all_user_list if (user.id != curr_user.id) and (
        user not in curr_user.friends_set.first().movie_friends.all())]
    if len(rec_friends) > 5:
        rec_friends = rec_friends[:5]

    return render(request, 'movies/friends.html', {'rec_friends': rec_friends})


def add_friend(request):
    if request.is_ajax():
        data = request.GET
        friend = User.objects.filter(id=data['user_id']).first()
        user = User.objects.filter(id=data['curr_user']).first()
        # 通过多对多关联来添加好友
        if bool(user.friends_set.all()):
            relationship = user.friends_set.first()
            relationship.movie_friends.add(friend)
        return JsonResponse({
            'status': 'success'
        })
    else:
        return Http404


def remove_friend(request):
    if request.is_ajax():
        data = request.GET
        friend = User.objects.filter(id=data['user_id']).first()
        user = User.objects.filter(id=data['curr_user']).first()
        if bool(user.friends_set.all()):
            relationship = user.friends_set.first()
            relationship.movie_friends.remove(friend)
        return JsonResponse({
            'status': 'success'
        })
    else:
        return Http404


@login_required
def liked_movies(request):
    return render(request, 'movies/liked_movies.html')


# @login_required
# def random_recommend(request):
#     movie_list = [movie for movie in Movie.objects.all().order_by("?")[
#         :100] if movie.cover]
#     context = {
#         'movie_list': movie_list,
#     }
#     return render(request, 'movies/movie_rec.html', context)


def movie_toggle_like(request):
    if request.is_ajax():

        data = request.GET
        movie = Movie.objects.filter(id=data['movie_id']).first()
        user = User.objects.filter(username=data['username']).first()

        flag = movie in user.moviepreference.favorite_movie.all()

        if flag:
            user.moviepreference.favorite_movie.remove(movie)
            front_end_mark = 'disliked'
        else:
            user.moviepreference.favorite_movie.add(movie)
            front_end_mark = 'liked'
        user.moviepreference.save()

        return JsonResponse({
            'status': front_end_mark,
            'flag': flag,
        })

    else:
        raise Http404


def movie_search(request):

    name = request.GET['movieName']
    current_url = request.GET['currentUrl']

    movie = Movie.objects.filter(name__startswith=name).first()

    if movie:
        return redirect('movies-detail', movie.id)

    elif name.replace(' ', ''):
        messages.warning(request, f'对不起， {name} 暂时不在我们的数据库中，请试一试其他电影名称')
        return redirect(current_url)
    else:
        return redirect(current_url)
