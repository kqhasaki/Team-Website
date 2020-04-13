from django.shortcuts import render
from .models import Movie
from django.views.generic import ListView, DetailView
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator
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
    # 默认的模板名称： <app>/<model>_<viewtype>.html
    tempalte_name = 'movies/movie_detail.html'


class RandomRecommendView(ListView):
    model = Movie
    template_name = 'movies/movie_rec.html'
    context_object_name = 'movie_list'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        # 我们需要先继承至父模板的get_context_data方法，否则我们有很多方法将不能使用
        context = super(ListView, self).get_context_data(**kwargs)
        # 然后添加自定义的参数
        context['is_random'] = True
        return context

    def get_queryset(self):
        return [movie for movie in self.model.objects.order_by('?')[:200] if movie.cover][:60]


def about(request):
    return render(request, 'movies/about.html')


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
