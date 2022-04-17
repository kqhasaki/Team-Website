from django.test import TestCase
from django.contrib.auth.models import User
from functools import reduce

# Create your tests here.


target_file = "./user_preferences.txt"
with open(target_file, 'w') as file:
    all_users = User.objects.all()
    for user in all_users:
        movie_list = list(map(lambda x: x.name, list(
            user.moviepreference.favorite_movie.all())))
        print(movie_list)
        if (movie_list):
            movie_list_str = reduce(
                lambda x, y: x + "," + y, movie_list)
        else:
            movie_list_str = "尚未收藏任何电影"

        line_str = user.username + "," + movie_list_str
        file.write(line_str)
