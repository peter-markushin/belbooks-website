from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('books', views.books, name='books-page'),
    path('books/<slug:slug>', views.book_detail, name='book-detail-page')
]