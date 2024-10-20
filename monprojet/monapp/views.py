from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.core.mail import send_mail
from django.urls import reverse_lazy

from monapp.forms import ContactUsForm, ProductAttributeForm, ProductForm, ProductItemForm, ProductAttributeValueForm
from .models import Product, ProductAttribute, ProductAttributeValue, ProductItem, Supplier, ProductSupplier, Cart, CartItem, Order, ValidatedCart, ValidatedCartItem, SupplierSellProduct
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q

class HomeView(TemplateView): 
    template_name = "home.html"
    def post(self, request, **kwargs):
        return render(request, self.template_name)  

class AboutView(TemplateView): 
    template_name = "about.html"
    def post(self, request, **kwargs):
        return render(request, self.template_name)

def ContactView(request):
    titreh1 = "Contact us !"
    if request.method=='POST':
        form = ContactUsForm(request.POST) 
        if form.is_valid():
            send_mail(
                subject=f'Message from {form.cleaned_data["name"] or "anonyme"} via MonProjet Contact Us form',
                message=form.cleaned_data['message'],
                from_email=form.cleaned_data['email'],
                recipient_list=['admin@monprojet.com'],
            )
            return redirect('home')
        else:
            form = ContactUsForm()
    else:
        form = ContactUsForm()
    return render(request, "contact.html",{'titreh1':titreh1, 'form':form})

class ProductListView(ListView): 
    model = Product
    template_name = "list_products.html" 
    context_object_name = "products"

    def get_context_data(self, **kwargs):
        get = self.request.GET
        search = get.get('search', '')
        print(search)

        context = super().get_context_data(**kwargs)
        context['titremenu'] = "Liste des produits"
        if search:
            products = Product.objects.filter(name__icontains=search)
        else:
            products = Product.objects.all()
        for product in products:
            product_suppliers = ProductSupplier.objects.filter(product=product)
            min_price = product_suppliers.aggregate(models.Min('price'))['price__min']
            product.min_price = min_price if min_price else 0
            total_quantity = product_suppliers.aggregate(models.Sum('quantity'))['quantity__sum']
            product.total_quantity = total_quantity if total_quantity else 0
        context['products'] = products
        return context

class ProductAttributeListView(ListView): 
    model = ProductAttribute
    template_name = "list_attributes.html" 
    context_object_name = "productattributes"
    def get_queryset(self):
        return ProductAttribute.objects.all().prefetch_related('productattributevalue_set')

    def get_context_data(self, **kwargs):
        context = super(ProductAttributeListView, self).get_context_data(**kwargs) 
        context['titremenu'] = "Liste des attributs"
        return context

class ProductAttributeDetailView(DetailView): 
    model = ProductAttribute
    template_name = "detail_attribute.html" 
    context_object_name = "productattribute"

    def get_context_data(self, **kwargs):
        context = super(ProductAttributeDetailView, self).get_context_data(**kwargs)
        context['titremenu'] = "Détail attribut" 
        context['values']=ProductAttributeValue.objects.filter(product_attribute=self.object).order_by('position') 
        return context

class ProductDetailView(DetailView): 
    model = Product
    template_name = "detail_product.html" 
    context_object_name = "product"
    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs) 
        context['titremenu'] = "Détail produit"
        product_suppliers = ProductSupplier.objects.filter(product=self.object)
        context['product_suppliers'] = product_suppliers
        return context

class SupplierDetailView(DetailView):
    model = Supplier
    template_name = "detail_supplier.html"
    context_object_name = "supplier"

    def get_context_data(self, **kwargs):
        context = super(SupplierDetailView, self).get_context_data(**kwargs)
        context['titremenu'] = "Détail fournisseur"
        products = self.object.products.all()
        context['products'] = products
        for product in products:
            product_supplier = ProductSupplier.objects.filter(product=product, supplier=self.object).first()
            product.price = product_supplier.price
        return context

class ConnectView(LoginView):
    template_name = 'login.html'
    def post(self, request, **kwargs):
        username = request.POST.get('username', False)
        password = request.POST.get('password', False)
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            return render(request, 'home.html')
        else:
            # On regarde si l'utilisateur n'est pas un fournisseur
            supplier = Supplier.objects.filter(name=username, password=password).first()
            if supplier:
                # mettre supplier dans la session
                request.session['supplier'] = supplier.id
                return redirect('home')
            # clear les messages d'erreur
            messages.error(request, None)
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect")
            return render(request, 'login.html')

class RegisterView(TemplateView): 
    template_name = 'register.html'
    def post(self, request, **kwargs):
        username = request.POST.get('username', False)
        mail = request.POST.get('mail', False)
        password = request.POST.get('password', False)
        user = User.objects.create_user(username, mail, password) 
        user.save()
        if user is not None and user.is_active:
            return render(request, 'login.html')
        else:
            return render(request, 'register.html')

class DisconnectView(TemplateView): 
    template_name = 'logout.html'
    def get(self, request, **kwargs): 
        # On regarde si l'utilisateur n'est pas un fournisseur
        if 'supplier' in request.session:
            del request.session['supplier']
        logout(request)
        return render(request, self.template_name)

class ProductCreateView(CreateView): 
    model = Product
    form_class=ProductForm
    template_name = "new_product.html"

    def form_valid(self, form: BaseModelForm) -> HttpResponse: 
        product = form.save()
        return redirect('detail_product', product.id)

class AttributeCreateView(CreateView):
    model = ProductAttribute
    form_class = ProductAttributeForm
    template_name = "new_attribute.html"

    def form_valid(self, form: ProductAttributeForm) -> HttpResponse:
        attribute = form.save()
        return redirect('detail_attribut', attribute.id)    

class ProductUpdateView(UpdateView): 
    model = Product
    form_class=ProductForm
    template_name = "update_product.html"

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        product = form.save()
        return redirect('detail_product', product.id)

class AttributeUpdateView(UpdateView):
    model = ProductAttribute
    form_class = ProductAttributeForm
    template_name = "update_attribute.html"

    def form_valid(self, form: ProductAttributeForm) -> HttpResponse:
        attribute = form.save()
        return redirect('detail_attribut', attribute.id)

class ProductDeleteView(DeleteView): 
    model = Product
    template_name = "delete_product.html" 
    success_url = reverse_lazy('produits')

class AttributeDeleteView(DeleteView):
    model = ProductAttribute
    template_name = "delete_attribute.html"
    success_url = reverse_lazy('attributs')

class ProductItemListView(ListView): 
    model = ProductItem
    template_name = "list_items.html" 
    context_object_name = "productitems"

    def get_queryset(self ):
        return ProductItem.objects.select_related('product').prefetch_related('attributes')

    def get_context_data(self, **kwargs):
        context = super(ProductItemListView, self).get_context_data(**kwargs) 
        context['titremenu'] = "Liste des déclinaisons"
        return context

class ProductItemDetailView(DetailView): 
    model = ProductItem
    template_name = "detail_item.html" 
    context_object_name = "productitem"

    def get_context_data(self, **kwargs):
        context = super(ProductItemDetailView, self).get_context_data(**kwargs) 
        context['titremenu'] = "Détail déclinaison"
        #Récupérer les attributs associés à cette déclinaison 
        context['attributes'] = self.object.attributes.all()
        return context

class ProductItemCreateView(CreateView):
    model = ProductItem
    form_class = ProductItemForm
    template_name = "new_item.html"

    def form_valid(self, form: ProductItemForm) -> HttpResponse:
        item = form.save()
        return redirect('detail_item', item.id)

class ProductItemUpdateView(UpdateView):
    model = ProductItem
    form_class = ProductItemForm
    template_name = "update_item.html"

    def form_valid(self, form: ProductItemForm) -> HttpResponse:
        item = form.save()
        return redirect('detail_item', item.id)

class ProductItemDeleteView(DeleteView):
    model = ProductItem
    template_name = "delete_item.html"
    success_url = reverse_lazy('items')

class ProductAttributeValueCreateView(CreateView):
    model = ProductAttributeValue
    form_class = ProductAttributeValueForm
    template_name = "new_value.html"

    def form_valid(self, form: ProductAttributeValueForm) -> HttpResponse:
        value = form.save()
        return redirect('detail_attribut', value.product_attribute.id)

class ProductAttributeValueUpdateView(UpdateView):
    model = ProductAttributeValue
    form_class = ProductAttributeValueForm
    template_name = "update_value.html"

    def form_valid(self, form: ProductAttributeValueForm) -> HttpResponse:
        value = form.save()
        return redirect('detail_attribut', value.product_attribute.id)

class ProductAttributeValueDeleteView(DeleteView):
    model = ProductAttributeValue
    template_name = "delete_value.html"
    def get_success_url(self):
        return reverse_lazy('detail_attribut', kwargs={'pk': self.object.product_attribute.id})

class ProductAttributeValueListView(ListView): 
    model = ProductAttributeValue
    template_name = "list_values.html" 
    context_object_name = "productattributevalues"

    def get_queryset(self ):
        return ProductAttributeValue.objects.select_related('product_attribute')

    def get_context_data(self, **kwargs):
        context = super(ProductAttributeValueListView, self).get_context_data(**kwargs) 
        context['titremenu'] = "Liste des valeurs d'attribut"
        return context

class ProductAttributeValueDetailView(DetailView): 
    model = ProductAttributeValue
    template_name = "detail_value.html" 
    context_object_name = "productattributevalue"

    def get_context_data(self, **kwargs):
        context = super(ProductAttributeValueDetailView, self).get_context_data(**kwargs) 
        context['titremenu'] = "Détail valeur d'attribut"
        return context

@login_required
def cart_detail(request):
    cart = Cart.objects.filter(user=request.user).first()
    cart_items = CartItem.objects.filter(cart=cart)
    if not cart:
        cart = Cart.objects.create(user=request.user)
    return render(request, 'cart_detail.html', {'cart': cart, 'total_price': cart.total_price, 'cart_items': cart_items})

@login_required
def add_to_cart(request, product_supplier_id):
    product_supplier = ProductSupplier.objects.get(id=product_supplier_id)
    cart = Cart.objects.filter(user=request.user).first()
    if not cart:
        cart = Cart.objects.create(user=request.user)
    product_cart = CartItem.objects.filter(cart=cart, product_supplier=product_supplier).first()
    if product_cart:
        if product_supplier.quantity > product_cart.quantity:
            cart.add_product(product_supplier)
            return redirect('cart_detail')
        else:
            messages.error(request, f"La quantité demandée pour {product_supplier.product.name} dépasse le stock disponible.", extra_tags=str(product_supplier.id))
            return redirect('detail_product', product_supplier.product.id)
    else:
        cart.add_product(product_supplier)
        return redirect('cart_detail')

@login_required
def update_cart(request, product_supplier_id):
    quantity = request.POST.get('quantity', 1)
    quantity = int(quantity)
    product_supplier = ProductSupplier.objects.get(id=product_supplier_id)
    cart = Cart.objects.filter(user=request.user).first()
    if cart:
        cart.update_quantity(product_supplier, quantity)
    return redirect('cart_detail')

class OrderValidationView(TemplateView):
    template_name = "order_validation.html"
    def get_context_data(self, **kwargs):
        context = super(OrderValidationView, self).get_context_data(**kwargs)
        cart = Cart.objects.filter(user=self.request.user).first()
        context['cart'] = cart
        context['total_price'] = cart.total_price
        return context

@login_required
def remove_from_cart(request, product_supplier_id):
    product_supplier = ProductSupplier.objects.get(id=product_supplier_id)
    cart = Cart.objects.filter(user=request.user).first()
    if cart:
        cart.remove_product(product_supplier)
    return redirect('cart_detail')

@login_required
def clear_cart(request):
    cart = Cart.objects.filter(user=request.user).first()
    if cart:
        cart.clear_cart()
    return redirect('cart_detail')

@login_required
def validate_order(request):
    cart = Cart.objects.filter(user=request.user).first()
    stock_disp = True
    for item in cart.items.all():
        if item.product_supplier.quantity < item.quantity:
            stock_disp = False
            messages.error(request, f"La quantité demandée pour {item.product_supplier.product.name} dépasse le stock disponible.", extra_tags=str(item.product_supplier.id))

    if cart:
        if cart.total_price > 0 and stock_disp:
            validated_cart = ValidatedCart.objects.create(
                user=request.user, 
                date_of_purchase=timezone.now(), 
                total_price=cart.total_price)
            for item in cart.items.all():
                product_supplier = ProductSupplier.objects.get(id=item.product_supplier.id)
                product_supplier.quantity -= item.quantity
                product_supplier.save()
                validated_cart_item = ValidatedCartItem.objects.create(
                    validated_cart=validated_cart,
                    product_supplier=item.product_supplier,
                    quantity=item.quantity
                )
                validated_cart_item.save()
            cart.clear_cart()
        else:
            if cart.total_price == 0:
                messages.error(request, "Votre panier est vide.")
            return redirect('cart_detail')
    return redirect('order_validation')

class HistoryCartsView(ListView):
    model = ValidatedCart
    template_name = "history_carts.html"
    context_object_name = "validated_carts"
    
    def get_queryset(self):
        return ValidatedCart.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(HistoryCartsView, self).get_context_data(**kwargs)
        context['titremenu'] = "Historique des achats"
        return context

# Admin views

class SupplierListView(TemplateView):
    template_name = "admin/fournisseur.html"
    def get(self, request, **kwargs):
        search = request.GET.get('search', '')
        if search:
            suppliers = Supplier.objects.filter(name__icontains=search)
        else:
            suppliers = Supplier.objects.all()
        return render(request, self.template_name, {'suppliers': suppliers})

# edit supplier

class SupplierUpdateView(UpdateView):
    model = Supplier
    fields = ['name', 'address', 'phone', 'email']
    template_name = "admin/edit_fournisseur.html"

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        supplier = form.save()
        return redirect('suppliers')

# delete supplier

class SupplierDeleteView(DeleteView):
    model = Supplier
    template_name = "admin/delete_fournisseur.html"
    success_url = reverse_lazy('suppliers')

# add supplier

class SupplierCreateView(CreateView):
    model = Supplier
    fields = ['name', 'address', 'phone', 'email', 'password']
    template_name = "admin/new_fournisseur.html"

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        supplier = form.save()
        return redirect('suppliers')

class OrderListView(TemplateView):
    template_name = "admin/orders.html"
    def get(self, request, **kwargs):
        search = request.GET.get('search', '')
        if search:
            orders = Order.objects.filter(Q(product__name__icontains=search) | Q(supplier__name__icontains=search))
        else:
            orders = Order.objects.all()
        return render(request, self.template_name, {'orders': orders})

# Order Add View

class OrderCreateView(CreateView):
    model = Order
    fields = ['product', 'supplier', 'quantity']
    template_name = "admin/new_order.html"

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        order = form.save()
        return redirect('orders')

# Views Supplier

class SupplierOrderListView(TemplateView):
    template_name = 'supplier/orders_by_supplier.html'
    # Regarde dans la session si le fournisseur est connecté
    def get(self, request, **kwargs):
        supplier_id = request.session.get('supplier')
        if not supplier_id:
            return redirect('login')
        order = Order.objects.filter(supplier_id=supplier_id)
        return render(request, self.template_name, {'orders': order})

class ChangeStatusOrder(TemplateView):
    def post(self, request, **kwargs):        
        order_id = kwargs.get('order_id')
        order = Order.objects.get(id=order_id)
        print(order.status)
        if order.status == 0:
            order.status = 1
        elif order.status == 1:
            order.status = 2
        elif order.status == 2 and not order.mis_en_stock:
            print(order.mis_en_stock)
            order.mis_en_stock = True
            order.save()
            # Ajouté la quantité commandée au stock du fournisseur
            try:
                product_supplier = ProductSupplier.objects.get(product=order.product, supplier=order.supplier)
                product_supplier.quantity += order.quantity
                product_supplier.save()
            except ProductSupplier.DoesNotExist:
                price = SupplierSellProduct.objects.get(product=order.product, supplier=order.supplier).price
                ProductSupplier.objects.create(product=order.product, supplier=order.supplier, quantity=order.quantity, price = price)
            return redirect('orders')
        
        order.save()
        return redirect('supplier_orders')

class SupplierProdcutSellView(TemplateView):
    template_name = 'supplier/sell_product.html'
    def get(self, request, **kwargs):
        supplier_id = request.session.get('supplier')
        if not supplier_id:
            return redirect('login')
        supplier = Supplier.objects.get(id=supplier_id)
        productsSell = SupplierSellProduct.objects.filter(supplier=supplier)
        print(productsSell)
        return render(request, self.template_name, {'products': productsSell})

class SupplierProductSellUpdate(UpdateView):
    model = SupplierSellProduct
    fields = ['price']
    template_name = "supplier/update_sell_product.html"

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        product_sell = form.save()
        return redirect('supplier_products')

class SupplierProductSellDelete(DeleteView):
    model = SupplierSellProduct
    template_name = "supplier/delete_sell_product.html"
    success_url = reverse_lazy('supplier_products')

class SupplierProductSellCreate(CreateView):
    model = SupplierSellProduct
    fields = ['product', 'price']
    template_name = "supplier/new_sell_product.html"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        supplier_id = self.request.session.get('supplier')
        if supplier_id:
            supplier = Supplier.objects.get(id=supplier_id)
            # Filtrer les produits qui ne sont pas déjà en vente par ce fournisseur
            form.fields['product'].queryset = Product.objects.exclude(
                id__in=SupplierSellProduct.objects.filter(supplier=supplier).values_list('product_id', flat=True)
            )
        return form

    def form_valid(self, form):
        supplier_id = self.request.session.get('supplier')
        if supplier_id:
            form.instance.supplier = Supplier.objects.get(id=supplier_id)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('supplier_products')