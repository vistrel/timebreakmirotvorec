from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from .models import Category, Person, StaticPage


def _pagination_query(request):
    params = request.GET.copy()
    params.pop('page', None)
    encoded = params.urlencode()
    return f'&{encoded}' if encoded else ''


def home(request):
    q = request.GET.get('q', '').strip()
    selected_category = request.GET.get('category', '').strip()

    persons = Person.objects.filter(is_published=True, show_on_homepage=True).select_related('category')

    if q:
        persons = persons.filter(
            Q(name__icontains=q)
            | Q(short_caption__icontains=q)
            | Q(description__icontains=q)
            | Q(reasoning__icontains=q)
            | Q(category__title__icontains=q)
        ).distinct()

    if selected_category:
        persons = persons.filter(category__slug=selected_category, category__is_active=True)

    paginator = Paginator(persons, 12)
    page_obj = paginator.get_page(request.GET.get('page'))

    context = {
        'page_obj': page_obj,
        'persons': page_obj.object_list,
        'categories': Category.objects.filter(is_active=True).order_by('sort_order', 'title'),
        'q': q,
        'selected_category': selected_category,
        'pagination_query': _pagination_query(request),
        'page_title': '',
        'page_description': '',
    }
    return render(request, 'catalog/home.html', context)


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug, is_active=True)
    q = request.GET.get('q', '').strip()

    persons = Person.objects.filter(is_published=True, category=category).select_related('category')
    if q:
        persons = persons.filter(
            Q(name__icontains=q)
            | Q(short_caption__icontains=q)
            | Q(description__icontains=q)
            | Q(reasoning__icontains=q)
        ).distinct()

    paginator = Paginator(persons, 12)
    page_obj = paginator.get_page(request.GET.get('page'))

    context = {
        'category': category,
        'page_obj': page_obj,
        'persons': page_obj.object_list,
        'q': q,
        'pagination_query': _pagination_query(request),
        'page_title': category.seo_title or category.title,
        'page_description': category.seo_description or category.short_description,
    }
    return render(request, 'catalog/category_detail.html', context)


def person_detail(request, slug):
    person = get_object_or_404(
        Person.objects.select_related('category').filter(is_published=True),
        slug=slug,
    )

    context = {
        'person': person,
        'page_title': person.seo_title or person.name,
        'page_description': person.seo_description or person.short_caption,
    }
    return render(request, 'catalog/person_detail.html', context)


def static_page(request, slug):
    page = get_object_or_404(StaticPage, slug=slug, is_published=True)
    context = {
        'page': page,
        'page_title': page.seo_title or page.title,
        'page_description': page.seo_description or page.title,
    }
    return render(request, 'catalog/static_page.html', context)
