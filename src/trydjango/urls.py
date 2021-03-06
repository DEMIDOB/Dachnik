"""trydjango URL Configuration

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
from pages.api import homepage_view, page404_view, favicon_view, order_help_view
from products.api import products_view, product_detail_view, categories_view
from feedback.api import process_feedback_view
from cart.api import user_cart_view, add_to_cart_view, remove_from_cart, update_cart
from order.api import make_order_view, complete_order, thankyou_view, remove_order, rm_o, recieve_order_view, rec_o
from customers.api import myname_api
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', homepage_view, name='home'),
    path('products/', products_view),
    path('products/product', product_detail_view),
    path('pf/', process_feedback_view),
    path('cart/', user_cart_view),
    path('cart/add/', add_to_cart_view),
    path('cart/remove/', remove_from_cart),
    path('order/', make_order_view),
    path('complete_order/', complete_order),
    path('404/', page404_view),
    path('thankyou/', thankyou_view),
    path('remove_order/', remove_order),
    path('rm_o', rm_o),
    path('favicon.ico/', favicon_view),
    path('recieve_order/', recieve_order_view),
    path('rec_o/', rec_o),
    path('help/order/', order_help_view),
    path('cart/update/', update_cart),
    path('cats/', categories_view),

    # USER DATA:
    path('myname/', myname_api)
]
