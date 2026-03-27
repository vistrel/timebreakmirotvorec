from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('category/<str:slug>/', views.category_detail, name='category_detail'),
    path('person/<str:slug>/', views.person_detail, name='person_detail'),
    path('pages/<str:slug>/', views.static_page, name='static_page'),
]
