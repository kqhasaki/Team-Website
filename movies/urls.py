from django.urls import path
from .views import MoiveListView, MovieDetailView, RandomRecommendView
from . import views


urlpatterns = [
    path('', MoiveListView.as_view(), name='movies-home'),
    # path('movies/movie_rec', views.random_recommend, name='movies-rec'),
    path('movies/movie_rec', RandomRecommendView.as_view(), name='movies-rec'),
    path('movies/<int:pk>/', MovieDetailView.as_view(), name='movies-detail'),
    path('about/', views.about, name='movies-about'),
    path('movies/liked_movies', views.liked_movies, name="liked-movies"),
]
