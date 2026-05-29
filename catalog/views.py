from django.shortcuts import render, get_object_or_404
from .models import Category, Product


def home(request):
    featured = Product.objects.filter(is_featured=True, is_available=True).prefetch_related('images')[:6]
    categories = Category.objects.all()
    context = {
        'featured_products': featured,
        'categories': categories,
        'page': 'home',
    }
    return render(request, 'home.html', context)


def shop(request):
    products = Product.objects.filter(is_available=True).prefetch_related('images').select_related('category')
    categories = Category.objects.all()

    # Filter by category slug if provided
    category_slug = request.GET.get('category', '')
    selected_category = None
    if category_slug:
        selected_category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=selected_category)

    context = {
        'products': products,
        'categories': categories,
        'selected_category': selected_category,
        'page': 'shop',
    }
    return render(request, 'shop.html', context)


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_available=True)
    images = product.images.all()
    related = Product.objects.filter(
        category=product.category,
        is_available=True
    ).exclude(pk=product.pk).prefetch_related('images')[:4]

    context = {
        'product': product,
        'images': images,
        'related_products': related,
        'sizes': product.get_sizes_list(),
        'colors': product.get_colors_list(),
        'page': 'shop',
    }
    return render(request, 'product_detail.html', context)


def about(request):
    return render(request, 'about.html', {'page': 'about'})


def contact(request):
    return render(request, 'contact.html', {'page': 'contact'})


def policies(request):
    return render(request, 'policies.html', {'page': 'policies'})
