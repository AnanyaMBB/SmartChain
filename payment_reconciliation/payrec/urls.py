from django.urls import path
from . import views

urlpatterns = [
    path('/index', views.indexPage, name='indexPage'),
    path('', views.home, name='home'),

    path('createProduct/', views.createProduct, name='createProduct'),
    path('register/', views.registerUser, name='createUser'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('home/', views.home, name='home'),
    path('product/<str:pk>/', views.product, name='product'),
    path('add/', views.addEntity, name='addEntity')



    # path('ac/', views.acPage, name='acPage'),
    # path('fans/', views.fans, name='fans'),
    # path('ducts/', views.ducts, name='ducts')
]
