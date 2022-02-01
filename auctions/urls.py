from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('create',views.createListing, name='create'),
    path('products/<str:list_id>',views.ListingPage, name='listingPage'),
    path('watchlist/<str:auction_id>',views.watchlist,name='watchlist'),
    path('delete/<str:id>',views.delete,name='delete'),
    path('close/<str:id>',views.close,name='close'),
    path('comments/<str:id>',views.comments,name='comments'),
    path('categories',views.categories,name='categories'),
    path('categories/<str:name>',views.listCategory,name='listCategory'),
    
]
