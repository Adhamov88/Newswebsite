from django.shortcuts import render

from .models import News


def context_processor(request):
    last_news = News.published.all().order_by('-publish_time')[:8]
    news_list = News.published.all().order_by('-publish_time')[:5]
    local_news = News.published.all().filter(category__name='Mahalliy')[:18]
    sport = News.published.all().filter(category__name='Sport')[:5]
    siyosat = News.published.all().filter(category__name='Siyosat')[:5]
    xorij = News.published.all().filter(category__name='Xorij')[:5]
    context = {
        'news_list': news_list,
        'local_news': local_news,
        'sport': sport,
        'siyosat': siyosat,
        'xorij': xorij,
        'last_news': last_news
    }
    return context
