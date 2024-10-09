from django.urls import path 
from . import views
from django.views.generic import *

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("about/", views.AboutView.as_view(), name="about"),
    path("contact/", views.ContactView, name="contact"),
    path("produits/", views.ProductListView.as_view(), name="produits"),
    path("produit/<pk>", views.ProductDetailView.as_view(), name="detail_product"),
    path('login/', views.ConnectView.as_view(), name='login'), 
    path('register/', views.RegisterView.as_view(), name='register'),
    path('logout/', views.DisconnectView.as_view(), name='logout'),
    path("produit/add/",views.ProductCreateView.as_view(), name="new_product"),
    path("produit/<pk>/update/",views.ProductUpdateView.as_view(), name="update_product"),
    path("produit/<pk>/delete/",views.ProductDeleteView.as_view(), name="delete_product"),
    path("attribut/", views.ProductAttributeListView.as_view(), name="attributs"),
    path("attribut/<pk>", views.ProductAttributeDetailView.as_view(), name="detail_attribut"),
    path("attribut/<pk>/update/", views.AttributeUpdateView.as_view(), name="update_attribut"),
    path("attribut/<pk>/delete/", views.AttributeDeleteView.as_view(), name="delete_attribut"),
    path("attribut/add/", views.AttributeCreateView.as_view(), name="new_attribut"),
    path("items/", views.ProductItemListView.as_view(), name="items"),
    path("item/<pk>", views.ProductItemDetailView.as_view(), name="detail_item"),
    path("item/add/", views.ProductItemCreateView.as_view(), name="new_item"),
    path("item/<pk>/update/", views.ProductItemUpdateView.as_view(), name="update_item"),
    path("item/<pk>/delete/", views.ProductItemDeleteView.as_view(), name="delete_item"),
]
