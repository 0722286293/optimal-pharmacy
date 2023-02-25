from posApp import views
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from django.views.generic.base import RedirectView

urlpatterns = [
    path('pos', views.pos, name="pos-page"),
    path('checkout-modal', views.checkout_modal, name="checkout-modal"),
    path('save-pos/', views.save_pos, name="save-pos"),
    path('receipt', views.receipt, name="receipt-modal"),
    path("notify/", views.notify, name="notify"),
]