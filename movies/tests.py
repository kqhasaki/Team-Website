from django.test import TestCase

# Create your tests here.
from .models import Movie

for obj in Movie.objects.all():
    if obj.cover and (not obj.is_valid(obj.cover)):
        print(f"{obj.name}封面失效")
        obj.cover = None
        obj.save()
        print(f"{obj.name}封面已删除")
