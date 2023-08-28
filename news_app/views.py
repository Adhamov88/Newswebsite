from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView

from .forms import ContactForm
from .models import News, Category
# Create your views here.


def list_view(request):
    news_list = News.published.all()
    context = {
        'news_list': news_list
    }
    return render(request, 'list_view.html', context)


def list_detail(request,news):
    list_detail = get_object_or_404(News, slug=news, status=News.Status.Published)
    context = {
        'list_detail': list_detail
    }
    return render(request, 'list_detail.html', context)


def index_view(request):
    news_list = News.published.all().order_by('-publish_time')[:5]
    category = Category.objects.all()
    local_news = News.published.all().filter(category__name='Mahalliy')[:5]
    sport = News.published.all().filter(category__name='Sport')[:5]
    siyosat = News.published.all().filter(category__name='Siyosat')[:5]
    xorij = News.published.all().filter(category__name='Xorij')[:5]
    context = {
        'news_list': news_list,
        'category': category,
        'local_news': local_news,
        'sport': sport,
        'siyosat': siyosat,
        'xorij': xorij
    }
    return render(request, 'index.html', context)
# def contact_view(request):
#     form=ContactForm(request.POST or None)
#     if request.method=='POST' and form.is_valid():
#         form.save()
#         return HttpResponse("biz bilan bog'langaniz uchun rahmat")
#     context={
#         'form':form
#     }
#     return render(request,'contact.html',context)


class contact_view(TemplateView):
    template_name = 'contact.html'

    def get(self, request, *args, **kwargs):
        form = ContactForm()
        context = {
            'form': form
        }
        return render(request, 'contact.html', context)

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if request.method == 'POST' and form.is_valid():
            form.save()
            return HttpResponse('Hush kebsiz')
        context = {
            'form': form
        }
        return render(request, 'contact.html', context)


def fail_view(request):
    context = {

    }
    return render(request, '404.html', context)


def about_view(request):
    context = {

    }
    return render(request, 'about.html', context)
class LocalNewsView(ListView):
    model = News
    template_name = 'local_news.html'
    context_object_name = 'mahalliy_yangiliklar'
    def get_queryset(self):
        name=News.published.all().filter(category__name='Mahalliy')
        return name
class HorijNewsView(ListView):
    model = News
    template_name = 'horij_news.html'
    context_object_name = 'Horij_yangiliklar'
    def get_queryset(self):
        name=News.published.all().filter(category__name='Xorij')
        return name
class SportNewsView(ListView):
    model = News
    template_name = 'sport_news.html'
    context_object_name = 'Sport_yangiliklar'
    def get_queryset(self):
        name=News.published.all().filter(category__name='Sport')
        return name
class PoliticalNewsViews(ListView):
    model = News
    template_name = 'political_news.html'
    context_object_name = 'siyosiy_yangiliklar'
    def get_queryset(self):
        name=News.published.all().filter(category__name='Siyosat')
        return name