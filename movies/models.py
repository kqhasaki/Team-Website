from django.db import models
# Create your models here.


class Movie(models.Model):
    movie_id = models.IntegerField(unique=True)
    name = models.TextField()
    alias = models.TextField(null=True)
    actors = models.TextField(null=True)
    cover = models.TextField(null=True)
    directors = models.TextField(null=True)
    douban_score = models.FloatField(null=True)
    douban_votes = models.IntegerField(null=True)
    imdb_id = models.TextField(null=True)
    languages = models.TextField(null=True)
    mins = models.IntegerField(null=True)
    official_site = models.TextField(null=True)
    regions = models.TextField(null=True)
    release_date = models.TextField(null=True)
    storyline = models.TextField(null=True)

    @staticmethod
    def is_valid(img_url):
        import requests
        response = requests.get(img_url)
        if response.status_code == 200:
            return True
        else:
            return False

    def get_baidu_cover(self, name):
        import string
        import json
        from random import choice
        from urllib.request import urlopen, quote

        name = name.replace(' ', '+')
        suffix = '电影海报'
        count_time_out = 0
        while True:
            print(name+suffix)
            url_path = f"https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord={name}{suffix}cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=0&hd=&latest=&copyright=&word={name}{suffix}"

            url_path = quote(url_path, safe=string.printable)

            with urlopen(url_path) as response:
                source = response.read().decode()
            try:
                data = json.loads(source)
                break
            except json.JSONDecodeError:
                suffix = ['海报', '图片', '电影', '', '百度', ' ',
                          '。', '+豆瓣', '+海报', '+图片', '百度图片'][count_time_out]
                count_time_out += 1
                if count_time_out == 12:
                    raise TimeoutError("图片找不到")
                continue

        for dict_imgs in data['data']:
            img_url = dict_imgs['thumbURL']
            if img_url and self.is_valid(img_url):
                return img_url
            else:
                continue

    def get_cover(self):
        self.cover = self.get_baidu_cover(self.name)

    class Meta:
        ordering = ['-douban_votes', '-douban_score']

    def __str__(self):
        if self.release_date and self.directors:
            return f'{self.name}------导演：{self.directors}, 上映日期：{self.release_date}'

        else:
            return self.name
