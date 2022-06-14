from django.views.generic.base import RedirectView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Product
from django.urls import reverse_lazy, reverse
from carts.models import CartItem
from django.db.models import Q

# Create your views here.

class Store(ListView):
    
    """ Vue servant à lister les articles disponible dans le shop.
        Ils sont trié en fonction des filtres appliqué par l'utilisateur.
    """
    model = Product
    context_object_name = "products"
    template_name = "store/store.html"  
    paginate_by = 6
    ordering = 'id'

    def get_queryset(self, *args, **kwargs) :
        
        """ Fonction hérité de la class ListView et servant à renvoyer les articles présent dans le eShop.
            Les filtres appliqué par l'utilisateur sont stocker dans la session.

        Returns:
            QuerySet: La liste des articles à afficher dans le shop.
        """
        
        queryset = super().get_queryset()
        if (self.request.session.get("size") and len(self.request.session.get("size")) > 0) or (self.request.session.get("color") and len(self.request.session.get("color")) > 0) :
            if self.request.session.get("size") and len(self.request.session.get("size")) > 0 :
                sizes = self.request.session.get("size")
                queryset = queryset.filter(is_available=True, size_category_id__in=sizes)
            
            if self.request.session.get("color") and len(self.request.session.get("color")) > 0 :
                color = self.request.session.get("color")
                queryset = queryset.filter(is_available=True, color_category_id__in=color)
            
            return queryset

        return queryset.filter(is_available=True)

    def get_context_data(self, **kwargs):
        
        """ Fonction hérité de la class ListView servant à definir le context du template lié à cette vue.

        Returns:
            dict: Le context pouvant etre utilisé dans le template html
        """
        context = super().get_context_data(**kwargs)
        context['product_count'] = self.get_queryset().count()
        return context

class SearchStore(Store):
    
    """ Class héritant de la class Store et servant à renvoyer la liste des articles filtrer en fonction du champs text de recherche.
    """

    ordering = '-created_on'

    def get_queryset(self, *args, **kwargs) :
        
        """ Fonction hérité de la class Store et servant à renvoyer les articles présent dans le eShop.
            Si la description ou le nom de l'article contient le text tapé par l'utilisateur, alors l'article sera affiché.
            
        Returns:
            QuerySet: La liste des articles à afficher dans le shop.
        """
        
        queryset = super().get_queryset()
        
        if 'keyword' in self.request.GET: 
            keyword = self.request.GET['keyword']

            if keyword:
                queryset = queryset.filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))

        return queryset

    def get_context_data(self, **kwargs):
        
        """ Fonction hérité de la class Store servant à definir le context du template lié à cette vue.

        Returns:
            dict: Le context pouvant etre utilisé dans le template html
        """
        
        context = super().get_context_data(**kwargs)
        if 'keyword' in self.request.GET: 
            context['keyword'] = self.request.GET['keyword']

        return context

class ProductDetail(DetailView):
    
    """ Vue servant à afficher un produit en particulié dans le detail.
    """
    
    model = Product
    context_object_name = "product"
    template_name = "store/product_detail.html"

class ChangeSize(RedirectView):
    
    """ Vue servant à changer les données dans la session de l'utilisateur lorsque qu'il change les filtre lié à la taille d'une pellicule.
        Cette class hérite de la class RedirectView car directement après l'action de cette vue, une redirection doit etre effectué. Cette vue ne sert pas à afficher des données à l'utilisateur.
    """
    
    permanent = False
    query_string = True
    pattern_name = reverse_lazy("store:store")

    def get_redirect_url(self, size):
        
        """ Fonction hérité de la class RedirectView servant à rediriger l'utilisateur.
            On la redefini afin d'update la session avec les bonne données avant de rediriger l'utilisateur.
        """
        
        if not self.request.session.session_key :
            self.request.session.create()
        self.request.session.modified = True
        if not 'size' in self.request.session:
            self.request.session['size'] = [size]
        elif size not in self.request.session.get("size") :
            self.request.session['size'].append(size)
        else :
            self.request.session['size'].pop(self.request.session['size'].index(size))
        return reverse("store:store")

class ChangeColor(RedirectView):
    
    """ Vue servant à changer les données dans la session de l'utilisateur lorsque qu'il change les filtre lié à la couleur d'une pellicule
        Cette class hérite de la class RedirectView car directement après l'action de cette vue, une redirection doit etre effectué. Cette vue ne sert pas à afficher des données à l'utilisateur.
    """
    
    permanent = False
    query_string = True
    pattern_name = reverse_lazy("store:store")

    def get_redirect_url(self, color):
        
        """ Fonction hérité de la class RedirectView servant à rediriger l'utilisateur.
            On la redefini afin d'update la session avec les bonne données avant de rediriger l'utilisateur.
        """
        
        if not self.request.session.session_key :
            self.request.session.create()
        self.request.session.modified = True
        if not 'color' in self.request.session:
            self.request.session['color'] = [color]
        elif color not in self.request.session.get("color") :
            self.request.session['color'].append(color)
        else :
            self.request.session['color'].pop(self.request.session['color'].index(color))
        return reverse("store:store")