from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.core.mail import send_mail
from django.urls import reverse_lazy

from monapp.forms import ContactUsForm, ProductForm
from .models import Product, ProductAttribute, ProductAttributeValue, ProductItem
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User

def ListProducts(request):
    prdcts = Product.objects.all()
    return render(request, 'list_products.html', {'products': prdcts})

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

    def get_queryset(self ):
    # Surcouche pour filtrer les résultats en fonction de la recherche 
    # Récupérer le terme de recherche depuis la requête GET
        query = self.request.GET.get('search')
        if query:
            # Filtre les produits par nom (insensible à la casse) 
            return Product.objects.filter(name__icontains=query)

        # Si aucun terme de recherche, retourner tous les produits 
        return Product.objects.all()

    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs) 
        context['titremenu'] = "Liste des produits"
        return context

class ProductAttributeListView(ListView): 
    model = ProductAttribute
    template_name = "list_attributes.html" 
    context_object_name = "productattributes"
    def get_queryset(self ):
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
        return context

class ConnectView(LoginView):
    template_name = 'login.html'
    def post(self, request, **kwargs):
        username = request.POST.get('username', False)
        password = request.POST.get('password', False)
        user = authenticate(username=username, password=password) 
        if user is not None and user.is_active:
            login(request, user)
            return render(request, 'home.html')
        else:
            return render(request, 'register.html')

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
        logout(request)
        return render(request, self.template_name)

def ProductCreate(request):
    form = ProductForm()
    return render(request, "new_product.html", {'form': form})

def ProductCreate(request):
    if request.method == 'POST':
        form = ProductForm(request.POST) 
        if form.is_valid():
            product = form.save()
            return redirect('detail_product', product.id)
    else:
        form = ProductForm()
    return render(request, "new_product.html", {'form': form})

class ProductCreateView(CreateView): 
    model = Product
    form_class=ProductForm
    template_name = "new_product.html"

    def form_valid(self, form: BaseModelForm) -> HttpResponse: 
        product = form.save()
        return redirect('detail_product', product.id)

class AttributeCreateView(CreateView):
    model = ProductAttribute
    fields = ['name']
    template_name = "new_attribute.html"

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
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
    fields = ['name']
    template_name = "update_attribute.html"

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
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
    fields = ['product', 'attributes', 'code']
    template_name = "new_item.html"

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        item = form.save()
        return redirect('detail_item', item.id)

class ProductItemUpdateView(UpdateView):
    model = ProductItem
    fields = ['product', 'attributes', 'code']
    template_name = "update_item.html"

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        item = form.save()
        return redirect('detail_item', item.id)

class ProductItemDeleteView(DeleteView):
    model = ProductItem
    template_name = "delete_item.html"
    success_url = reverse_lazy('items')
