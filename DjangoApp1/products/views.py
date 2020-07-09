from django.shortcuts import render, redirect
from .models import Products, OrderItem, Order, BookImage
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from products.forms import ProductForm, ProductUpdateForm, ImageForm
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.utils import timezone
from django import template
from django.core.exceptions import ObjectDoesNotExist
from django.forms import modelformset_factory
from django.views.generic.edit import FormMixin

from statsd import StatsClient
stats = StatsClient()
import logging
logger = logging.getLogger(__name__)


class ProductList(ListView):
    model = Products
    template_name = "books/books.html"
    context_object_name = 'books'
    ordering = ['title', 'price', '-quantity']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['obj'] = BookImage.objects.all()
        return context


class ProductDetailItem(FormMixin, DetailView):
    model = Products
    template_name = "books/book.html"
    form_class = ImageForm

    def get_context_data(self, **kwargs):
        stats.incr('book-viewed')
        context = super().get_context_data(**kwargs)
        context['obj'] = BookImage.objects.filter(book=self.object.id)
        return context


class MyBooksList(ListView):
    model = Products
    template_name = "books/mybooks.html"
    context_object_name = 'books'
    ordering = ['title', 'price', '-quantity']


class ProductCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView, ):
    form_class = ProductForm
    model = Products
    template_name = 'books/new_book.html'
    success_message = "Books Added"

    def form_valid(self, form):
        timer = stats.timer('create-book')
        timer.start()
        form.instance.seller = self.request.user
        Products = form.save()
        logger.info("New Book added by user")
        Products.save()
        timer.stop()
        return super().form_valid(form)


class ImageAdd(LoginRequiredMixin, SuccessMessageMixin, CreateView, ):
    form_class = ImageForm
    model = BookImage
    template_name = 'books/add_image.html'
    success_message = "Image Added"
    success_url = '/books/'

    def form_valid(self, form):
        timer = stats.timer('image-added')
        timer.start()
        form.instance.book = Products.objects.get(pk=self.kwargs['pk'])
        BookImage = form.save()
        BookImage.save()
        logger.info("New Image added by user")
        timer.stop()
        return super().form_valid(form)


class ProductUpdate(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    form_class = ProductUpdateForm
    model = Products
    template_name = 'books/update_book.html'
    success_message = "Books Updated"

    def test_func(self):
        timer = stats.timer('update-book')
        timer.start()
        book = self.get_object()
        logger.info("Book is Updated my User")
        timer.stop()
        if self.request.user == book.seller:
            return True
        return False


class ProductDelete(LoginRequiredMixin, DeleteView):
    model = Products
    template_name = 'books/delete_book.html'
    success_url = '/books'
    
    def test_func(self):
        timer = stats.timer('product-deleted')
        timer.start()
        book = self.get_object()
        logger.info("Book Deleted by User")
        timer.stop()
        if self.request.user == book.seller:
            return True
        return False


def BookAddToCart(request, pk):
    if not request.user.is_authenticated:
        return redirect("login")
    item = get_object_or_404(Products, id=pk)
    cart_book, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False)
    cart = Order.objects.filter(user=request.user, ordered=False)
    if cart.exists():
        order = cart[0]
        # check if the order item is in the order
        if order.items.filter(item__id=item.pk).exists():
            if item.quantity == 0:
                messages.info(request, "Maximum amount of book added to the cart.")
                return redirect("cart")
            timer = stats.timer('book-added-to-cart')
            timer.start()
            cart_book.quantity += 1
            cart_book.save()
            item.quantity -= 1
            item.save()
            messages.info(request, "The Book is added to the cart.")
            logger.info("The Book is added to the cart.")
            timer.stop()
            return redirect("cart")
        else:
            timer = stats.timer('book-added-to-cart')
            timer.start()
            order.items.add(cart_book)
            item.quantity -= 1
            item.save()
            messages.info(request, "The Book is added to the cart.")
            logger.info("The Book is added to the cart.")
            timer.stop()
            return redirect("book_item", pk=pk)
    else:
        timer = stats.timer('book-added-to-cart')
        timer.start()
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(cart_book)
        item.quantity -= 1
        item.save()
        messages.info(request, "This item was added to your cart.")
        logger.info("The Book is added to the cart.")
        timer.stop()
        return redirect("cart")


def RemoveAllBooks(request, pk):
    book = get_object_or_404(Products, pk=pk)
    cart = Order.objects.filter(
        user=request.user,
        ordered=False)
    if cart.exists():
        order = cart[0]
        # check if the order item is in the order
        if order.items.filter(item__id=book.pk).exists():
            cart_book = OrderItem.objects.filter(
                item=book,
                user=request.user,
                ordered=False)[0]
            timer = stats.timer('books-removed-from-cart')
            timer.start()
            book.quantity += cart_book.quantity
            book.save()
            order.items.remove(cart_book)
            cart_book.delete()
            messages.info(request, "This item was removed from your cart.")
            logger.info( "The book was removed from your cart.")
            timer.stop()
            return redirect("cart")
        else:
            messages.info(request, "This item was not in your cart")
            logger.info( "The book was removed from your cart.")
            return redirect("book_item", pk=pk)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("book_item", pk=pk)


def BookRemoveFromCart(request, pk):
    book = get_object_or_404(Products, pk=pk)
    cart = Order.objects.filter(
        user=request.user,
        ordered=False)
    if cart.exists():
        order = cart[0]
        # check if the order item is in the order
        if order.items.filter(item__id=book.pk).exists():
            cart_book = OrderItem.objects.filter(
                item=book,
                user=request.user,
                ordered=False)[0]
            if cart_book.quantity > 1:
                timer = stats.timer('book-removed-from-cart')
                timer.start()
                cart_book.quantity -= 1
                cart_book.save()
                book.quantity += 1
                book.save()
                messages.info(request, "The Book was removed from the cart.")
                logger.info( "The Book was removed from your cart.")
                timer.stop()
                return redirect("cart")
            else:
                timer = stats.timer('book-removed-from-cart')
                timer.start()
                order.items.remove(cart_book)
                messages.info(request, "The Book was removed from the cart.")
                logger.info("The Book was removed from your cart.")
                book.quantity += 1
                book.save()
                timer.stop()
                return redirect("cart")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("cart")
    else:
        messages.info(request, "You do not have an active order")
        return redirect("cart")


def Cart(request):
    if not request.user.is_authenticated:
        return redirect("login")
    try:
        cart = Order.objects.get(user=request.user, ordered=False)
        context = {
            'object': cart
        }
        return render(request, 'books/order_summary.html', context)
    except ObjectDoesNotExist:
        messages.warning(request, "Cart is empty")
        return redirect("/books/")


class ImageDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = BookImage
    template_name = 'books/delete_image.html'
    success_url = '/books/'

    def test_func(self):
        timer = stats.timer('image-removed')
        timer.start()
        bookimage = self.get_object()
        logger.info( "This image was removed.")
        timer.stop()
        return True
