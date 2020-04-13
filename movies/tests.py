from django.test import TestCase

# Create your tests here.
from .models import Movie

for obj in Movie.objects.all():
    if obj.cover and obj.is_valid(obj.cover):
        print(f"{obj.name}链接有效")
    else:
        try:
            obj.get_cover()
        except:
            print(f"*******{obj.name}图片获取失败******")
            break
        else:
            obj.save()
            print(f"-------{obj.name}图片更新成功------")
