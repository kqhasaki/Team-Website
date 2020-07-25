from django.urls import path
from .views import MoiveListView, MovieDetailView
from . import views


urlpatterns = [
    path('', MoiveListView.as_view(), name='movies-home'),
    # path('movies/movie_rec', views.random_recommend, name='movies-rec'),
    path('movies/movie_rec', views.get_recommendation, name='movies-rec'),
    path('movies/movies-toggle-like', views.movie_toggle_like,
         name='movies-toggle-like'),
    path('movies/<int:pk>/', MovieDetailView.as_view(), name='movies-detail'),
    path('friends/', views.show_friends, name='movies-friends'),
    path('movies/liked_movies', views.liked_movies, name="liked-movies"),
    path('movies/search', views.movie_search, name="movies-search"),
    path('movies/add_friend', views.add_friend, name="add-friend"),
    path('movies/remove_friend', views.remove_friend, name="remove-friend"),
    path('movies/others_liked_moives',
         views.others_liked_moives, name="others-liked-movies")
]
