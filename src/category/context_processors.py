from category.models import ColorCategory, SizeCategory

def menu_links(request):
    links = ColorCategory.objects.all()
    size_categories = SizeCategory.objects.all()
    return dict(links=links, size_categories=size_categories)