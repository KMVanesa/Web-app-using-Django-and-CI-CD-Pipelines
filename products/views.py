from django.shortcuts import render, redirect
from .models import Products, OrderItem, Order
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from products.forms import ProductForm, ProductUpdateForm
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.utils import timezone
from django import template
from django.core.exceptions import ObjectDoesNotExist


class ProductList(ListView):
    model = Products
    template_name = "books/books.html"
    context_object_name = 'books'
    ordering = ['title', 'price', '-quantity']


class ProductDetailItem(DetailView):
    model = Products
    template_name = "books/book.html"


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

    # def post(self, request, *args, **kwargs):
    #     form_class = self.get_form_class()
    #     form = self.get_form(form_class)
    #     files = request.FILES.getlist('images')
    #     if form.is_valid():
    #         seller = request.user
    #         isbn = form.cleaned_data['isbn']
    #         title = form.cleaned_data['title']
    #         authors = form.cleaned_data['authors']
    #         publication_date = form.cleaned_data['publication_date']
    #         quantity = form.cleaned_data['quantity']
    #         price = form.cleaned_data['price']
    #         for f in files:
    #             Products.objects.create(images=f)
    #         return self.form_valid(form)
    #     else:
    #         return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.seller = self.request.user
        Products = form.save()

        Products.save()
        return super().form_valid(form)

    # def form_valid(self, form):
    #     obj = form.save(commit=False)
    #     if self.request.FILES:
    #         for f in self.request.FILES.getlist('images'):
    #             obj = self.model.objects.create(images=f)
    #     return super(ProductCreate, self).form_valid(form)


class ProductUpdate(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    form_class = ProductUpdateForm
    model = Products
    template_name = 'books/update_book.html'
    success_message = "Books Updated"

    def test_func(self):
        book = self.get_object()
        if self.request.user == book.seller:
            return True
        return False


class ProductDelete(LoginRequiredMixin, DeleteView):
    model = Products
    template_name = 'books/delete_book.html'
    success_url = '/books'

    def test_func(self):
        book = self.get_object()
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
            cart_book.quantity += 1
            cart_book.save()
            item.quantity -= 1
            item.save()
            messages.info(request, "The Book is added to the cart.")
            return redirect("cart")
        else:
            order.items.add(cart_book)
            item.quantity -= 1
            item.save()
            messages.info(request, "The Book is added to the cart.")
            return redirect("book_item", pk=pk)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(cart_book)
        item.quantity -= 1
        item.save()
        messages.info(request, "This item was added to your cart.")
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
            book.quantity += cart_book.quantity
            book.save()
            order.items.remove(cart_book)
            cart_book.delete()
            messages.info(request, "This item was removed from your cart.")
            return redirect("cart")
        else:
            messages.info(request, "This item was not in your cart")
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
                cart_book.quantity -= 1
                cart_book.save()
                book.quantity += 1
                book.save()
                messages.info(request, "The Book was removed from the cart.")
                return redirect("cart")
            else:
                order.items.remove(cart_book)
                messages.info(request, "The Book was removed from the cart.")
                book.quantity += 1
                book.save()
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
