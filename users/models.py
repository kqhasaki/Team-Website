from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.conf import settings
from functools import reduce

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to="profile_pics")

    def __str__(self):
        return f'{ self.user.username } Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


class Friends(models.Model):
    movie_friends = models.ManyToManyField(
        User, default=None)


class MoviePreference(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favorite_movie = models.ManyToManyField(
        'movies.Movie', default=None)

    def __str__(self):
        movie_list = [movie.name for movie in self.favorite_movie.all()]
        string = reduce(lambda x, y: x+','+y, movie_list)
        return f'{self.user.username}喜欢的电影: {string}'


# class MovieRecommendation(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     recommend_movies = models.ManyToManyField(
#         'movies.Movie'
#     )

#     def get_recommendation(self):
#         favortite_movie_list = self.user.moviepreference.favorite_movie.all()
#         # 这里写推荐函数，结合用户喜欢的电影，从Movie数据库中推荐电影
#         return get_rec_list(favortite_movie_list)
