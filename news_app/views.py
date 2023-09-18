from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, UpdateView, CreateView, DeleteView
from django import forms
from hitcount.utils import get_hitcount_model

from .OnlyLoginSuperRequierdMixin import OnlyLoginSuperUser
from .forms import ContactForm, CommentForm
from .models import News, Category
# Create your views here.


def list_view(request):
    news_list = News.published.all()
    context = {
        'news_list': news_list
    }
    return render(request, 'list_view.html', context)

from hitcount.views import HitCountDetailView, HitCountMixin


def list_detail(request, news):
    news = get_object_or_404(News, slug=news, status=News.Status.Published)
    context={

    }
    hit_count = get_hitcount_model().objects.get_for_object(news)

    hits = hit_count.hits
    hitcontext=context['hitcount'] = {'pk': hit_count.pk}
    hit_count_response = HitCountMixin.hit_count(request,hit_count)
    if hit_count_response.hit_counted:
        hits=hits+1
        hitcontext['hit_counted']=hit_count_response.hit_counted
        hitcontext['hit_message']=hit_count_response.hit_message
        hitcontext['total_hits']=hits
    comments = news.comments.filter(active=True)
    new_comment = None

    comment_count = comments.count()
    comment_form = CommentForm()  # Initialize with a default value

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.news = news
            new_comment.user = request.user
            new_comment.save()

    context = {
        'news': news,
        'comment_count':comment_count,
        'comments': comments[:5],
        'new_comment': new_comment,
        'comment_form': comment_form
    }
    return render(request, 'list_detail.html', context)

@login_required
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
class NewsUpdateView(OnlyLoginSuperUser,UpdateView):
    model=News
    fields = ('title','body','image','status','category')
    template_name = 'crud/news_edit.html'
class NewsDeleteView(OnlyLoginSuperUser,DeleteView):
    model = News
    template_name='crud/news_delete.html'
    success_url = reverse_lazy('index_view')




class NewsCreateView(OnlyLoginSuperUser,CreateView):
    model = News
    template_name = 'crud/news_create.html'
    fields = ('title', 'slug', 'image', 'status', 'body', 'category')

@login_required()
@user_passes_test(lambda u:u.is_superuser)
def adminpage(request):
    admin_users=User.objects.filter(is_superuser=True)
    context={
        'admin_users':admin_users
    }
    return render(request,'profile/admin_page.html',context)

class SearchResultList(ListView):
    model = News
    template_name = 'search_result.html'
    context_object_name = 'barcha_yangiliklar'
    def get_queryset(self):
        query=self.request.GET.get('q')
        return News.objects.filter(Q(title__icontains=query) | Q(body__icontains=query)
        )


