"""DjangoApp1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from first_app import views
from products import views as product_view
from products.views import ProductList, ProductDetailItem, ProductCreate, ProductUpdate, ProductDelete, MyBooksList, \
    ImageAdd, ImageDeleteView
from django.urls import include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name="index"),
    path('register/', views.register_form, name="register"),
    path('login/', views.user_login, name="login"),
    path('logout/', views.user_logout, name="logout"),
    path('update_profile/', views.profile, name="update"),
    path('first_app/', include('first_app.urls')),
    path('update_password/', views.change_password, name="password_change"),
    path('cart/', product_view.Cart, name='cart'),
    path('add-to-cart/<int:pk>/', product_view.BookAddToCart, name='add-to-cart'),
    path('remove-from-cart/<int:pk>/', product_view.RemoveAllBooks, name='remove-from-cart'),
    path('remove-item-from-cart/<int:pk>/', product_view.BookRemoveFromCart,
         name='remove-single-item-from-cart'),
    path('books/', ProductList.as_view(), name="books"),
    path('mybooks/', MyBooksList.as_view(), name="mybooks"),
    path('books/<int:pk>/', ProductDetailItem.as_view(), name="book_item"),
    path('books/new/', ProductCreate.as_view(), name="book_new"),
    path('books/<int:pk>/update/', ProductUpdate.as_view(), name="book_update"),
    path('books/<int:pk>/add-image/', ImageAdd.as_view(), name="add-image"),
    path('books/<int:pk>/delete/', ProductDelete.as_view(), name="book_delete"),
    path('book/<int:book>/deleteimage/<int:pk>/', ImageDeleteView.as_view(), name='delete-image'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
