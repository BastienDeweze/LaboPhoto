from django.shortcuts import render
from django.views.generic.list import ListView
from store.models import Product


def index (request):
    return render(request, "home.html")

class HomePage(ListView):
    model = Product
    context_object_name = "products"
    template_name = "home.html"
    # paginate_by = 4

    def get_queryset(self) :
        queryset = super().get_queryset()
        return queryset.filter(is_available=True)