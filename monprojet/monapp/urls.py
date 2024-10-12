from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .viewsAPI import ProductViewSet, StatusViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'statuses', StatusViewSet)

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("about/", views.AboutView.as_view(), name="about"),
    path("contact/", views.ContactView, name="contact"),
    path("produits/", views.ProductListView.as_view(), name="produits"),
    path("produit/<pk>", views.ProductDetailView.as_view(), name="detail_product"),
    path('login/', views.ConnectView.as_view(), name='login'), 
    path('register/', views.RegisterView.as_view(), name='register'),
    path('logout/', views.DisconnectView.as_view(), name='logout'),
    path("produit/add/", views.ProductCreateView.as_view(), name="new_product"),
    path("produit/<pk>/update/", views.ProductUpdateView.as_view(), name="update_product"),
    path("produit/<pk>/delete/", views.ProductDeleteView.as_view(), name="delete_product"),
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
    path("values/", views.ProductAttributeValueListView.as_view(), name="values"),
    path("value/<pk>", views.ProductAttributeValueDetailView.as_view(), name="detail_value"),
    path("value/add/", views.ProductAttributeValueCreateView.as_view(), name="new_value"),
    path("value/<pk>/update/", views.ProductAttributeValueUpdateView.as_view(), name="update_value"),
    path("value/<pk>/delete/", views.ProductAttributeValueDeleteView.as_view(), name="delete_value"),
    
    path('api/', include(router.urls)),
]