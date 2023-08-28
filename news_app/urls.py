from django.urls import path
from .views import (
    list_view,list_detail,index_view,contact_view,fail_view,about_view,LocalNewsView,HorijNewsView,SportNewsView,PoliticalNewsViews
)
urlpatterns=[
    path('news/',list_view,name='list_view'),
    path('/<slug:news>/',list_detail,name='list_detail'),
    path('',index_view,name='index_view'),
    path('contact/',contact_view.as_view(),name='contact_view'),
    path('fail/',fail_view,name='fail'),
    path('about/',about_view,name='about'),
    path('local_news/',LocalNewsView.as_view(),name='local_news'),
    path('horij_news/',HorijNewsView.as_view(),name='horij_news'),
    path('sport_news/',SportNewsView.as_view(),name='sport_news'),
    path('political_news/',PoliticalNewsViews.as_view(),name='political_news')
]