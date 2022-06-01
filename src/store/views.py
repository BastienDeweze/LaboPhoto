from django.views.generic.base import RedirectView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Product
from django.urls import reverse_lazy, reverse
from carts.models import CartItem
from django.db.models import Q

# Create your views here.

class Store(ListView):
    model = Product
    context_object_name = "products"
    template_name = "store/store.html"
    paginate_by = 6
    ordering = 'id'

    def get_queryset(self, *args, **kwargs) :
        queryset = super().get_queryset()
        if self.request.session.get("size") and len(self.request.session.get("size")) > 0 :
            sizes = self.request.session.get("size")
            return queryset.filter(is_available=True, size_category_id__in=sizes)

        return queryset.filter(is_available=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_count'] = self.get_queryset().count()
        return context

class SearchStore(Store):

    ordering = '-created_on'

    def get_queryset(self, *args, **kwargs) :
        queryset = super().get_queryset()
        
        if 'keyword' in self.request.GET: 
            keyword = self.request.GET['keyword']

            if keyword:
                queryset = queryset.filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'keyword' in self.request.GET: 
            context['keyword'] = self.request.GET['keyword']

        return context

class ProductDetail(DetailView):
    model = Product
    context_object_name = "product"
    template_name = "store/product_detail.html"

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        # context['in_cart'] = CartItem.objects.filter(cart__cart_id=self.request.user, product__slug=self.kwargs.get("slug")).exists()
        return context

class ChangeSize(RedirectView):
    
    permanent = False
    query_string = True
    pattern_name = reverse_lazy("store:store")

    def get_redirect_url(self, size):
        self.request.session.modified = True
        if not 'size' in self.request.session:
            self.request.session['size'] = [size]
        elif size not in self.request.session.get("size") :
            self.request.session['size'].append(size)
        else :
            self.request.session['size'].pop(self.request.session['size'].index(size))
        return reverse("store:store")