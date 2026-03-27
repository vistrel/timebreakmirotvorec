from .models import Category, SiteSettings, StaticPage, TextBlock


def global_site_context(request):
    site_settings, _ = SiteSettings.objects.get_or_create(
        pk=1,
        defaults={
            'site_name': 'MineCatalog',
            'site_tagline': 'Гибкий каталог персоналий',
            'default_seo_title': 'MineCatalog',
            'default_seo_description': 'Каталог персоналий с гибкими категориями и редакционными пояснениями.',
        },
    )
    site_blocks = {
        block.key: block
        for block in TextBlock.objects.filter(is_active=True)
    }
    nav_pages = StaticPage.objects.filter(is_published=True, show_in_nav=True).order_by('sort_order', 'title')
    footer_pages = StaticPage.objects.filter(is_published=True, show_in_footer=True).order_by('sort_order', 'title')
    nav_categories = Category.objects.filter(is_active=True, persons__is_published=True).distinct().order_by('sort_order', 'title')

    return {
        'site_settings': site_settings,
        'site_blocks': site_blocks,
        'nav_pages': nav_pages,
        'footer_pages': footer_pages,
        'nav_categories': nav_categories,
    }
