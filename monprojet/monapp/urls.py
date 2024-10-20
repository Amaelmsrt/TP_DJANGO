from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .viewsAPI import ProductViewSet, StatusViewSet, SupplierSellProductViewSet, SupplierViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'status', StatusViewSet)
router.register(r'supplier_sell_product', SupplierSellProductViewSet)
router.register(r'suppliers', SupplierViewSet)



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
    path("supplier/<pk>/", views.SupplierDetailView.as_view(), name="detail_supplier"),
    path('add_to_cart/<int:product_supplier_id>/', views.add_to_cart, name='add_to_cart'),
    path('update_cart/<int:product_supplier_id>/', views.update_cart, name='update_cart'),
    path('remove_from_cart/<int:product_supplier_id>/', views.remove_from_cart, name='remove_from_cart'),
    path("cart/", views.cart_detail, name="cart_detail"),
    path("order/validate/", views.OrderValidationView.as_view(), name="order_validation"),
    path("validate_order/", views.validate_order, name="validate_order"),
    path('admin-fournisseur/', views.SupplierListView.as_view(), name='suppliers'),
    path('admin-fournisseur/add/', views.SupplierCreateView.as_view(), name='new_supplier'),
    path('admin-fournisseur/<pk>/update/', views.SupplierUpdateView.as_view(), name='update_supplier'),
    path('admin-fournisseur/<pk>/delete/', views.SupplierDeleteView.as_view(), name='delete_supplier'),
    path('admin-order/', views.OrderListView.as_view(), name='orders'),
    path('admin-order/add/', views.OrderCreateView.as_view(), name='new_order'),
    path('supplier-order/', views.SupplierOrderListView.as_view(), name='supplier_orders'),
    path('supplier-product-selling/', views.SupplierProdcutSellView.as_view(), name='supplier_products'),
    path('supplier-product-selling/<pk>/update/', views.SupplierProductSellUpdate.as_view(), name='update_supplier_product'),
    path('supplier-product-selling/<pk>/delete/', views.SupplierProductSellDelete.as_view(), name='delete_supplier_product'),
    path('supplier-product-selling/add/', views.SupplierProductSellCreate.as_view(), name='new_supplier_product'),
    path('orders/change_status/<int:order_id>/', views.ChangeStatusOrder.as_view(), name='change_status_order'),
    path('carts/history/', views.HistoryCartsView.as_view(), name='history_carts'),

    path('api/', include(router.urls)),
]
