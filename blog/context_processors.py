from .models import Category
def menu_categories(request):
    categories = Category.objects.all()
    print(type(categories))
    print(categories.first())
    return {
        'categories': categories
    }
