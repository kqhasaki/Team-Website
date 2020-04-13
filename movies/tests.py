from django.test import TestCase

# Create your tests here.
from .models import Movie

test_list = Movie.objects.all()[:5]

for test_obj in test_list:
    test_obj.get_cover()

for test_obj in test_list:
    print(test_obj.cover)
