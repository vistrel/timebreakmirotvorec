from django.contrib import admin
from django.utils.html import format_html

from .models import Category, Person, SiteSettings, StaticPage, TextBlock


admin.site.site_header = 'MineCatalog Admin'
admin.site.site_title = 'MineCatalog Admin'
admin.site.index_title = 'Управление каталогом'


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Основное', {'fields': ('site_name', 'site_tagline')}),
        ('SEO', {'fields': ('default_seo_title', 'default_seo_description')}),
        ('Контакты и футер', {'fields': ('contacts_email', 'contacts_telegram', 'footer_text', 'copyright_text')}),
        ('Служебное', {'fields': ('updated_at',)}),
    )
    readonly_fields = ('updated_at',)

    def has_add_permission(self, request):
        if SiteSettings.objects.exists():
            return False
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(TextBlock)
class TextBlockAdmin(admin.ModelAdmin):
    list_display = ('title', 'key', 'is_active', 'updated_at')
    list_filter = ('is_active',)
    search_fields = ('title', 'key', 'content')
    readonly_fields = ('updated_at',)


@admin.action(description='Опубликовать выбранные карточки')
def publish_persons(modeladmin, request, queryset):
    queryset.update(is_published=True)


@admin.action(description='Снять с публикации выбранные карточки')
def unpublish_persons(modeladmin, request, queryset):
    queryset.update(is_published=False)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'sort_order', 'is_active', 'updated_at')
    list_filter = ('is_active',)
    search_fields = ('title', 'slug', 'short_description', 'description')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Основное', {'fields': ('title', 'slug', 'short_description', 'description')}),
        ('SEO', {'fields': ('seo_title', 'seo_description')}),
        ('Публикация', {'fields': ('sort_order', 'is_active')}),
        ('Служебное', {'fields': ('created_at', 'updated_at')}),
    )


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'category',
        'status_label',
        'is_published',
        'show_on_homepage',
        'sort_order',
        'updated_at',
    )
    list_filter = ('is_published', 'show_on_homepage', 'category')
    search_fields = ('name', 'slug', 'short_caption', 'description', 'reasoning', 'sources_notes')
    readonly_fields = ('image_preview', 'created_at', 'updated_at')
    actions = [publish_persons, unpublish_persons]
    fieldsets = (
        ('Основное', {'fields': ('name', 'slug', 'category', 'status_label', 'short_caption', 'image', 'image_preview')}),
        ('Текст карточки', {'fields': ('description', 'reasoning', 'extra_information', 'sources_notes', 'editorial_note')}),
        ('SEO', {'fields': ('seo_title', 'seo_description')}),
        ('Публикация', {'fields': ('is_published', 'show_on_homepage', 'sort_order')}),
        ('Служебное', {'fields': ('created_at', 'updated_at')}),
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-width: 180px; border: 1px solid #999;" />', obj.image.url)
        return 'Нет изображения'

    image_preview.short_description = 'Превью'


@admin.action(description='Опубликовать выбранные страницы')
def publish_pages(modeladmin, request, queryset):
    queryset.update(is_published=True)


@admin.action(description='Снять с публикации выбранные страницы')
def unpublish_pages(modeladmin, request, queryset):
    queryset.update(is_published=False)


@admin.register(StaticPage)
class StaticPageAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'is_published', 'show_in_nav', 'show_in_footer', 'updated_at')
    list_filter = ('is_published', 'show_in_nav', 'show_in_footer')
    search_fields = ('title', 'slug', 'body')
    readonly_fields = ('created_at', 'updated_at')
    actions = [publish_pages, unpublish_pages]
    fieldsets = (
        ('Основное', {'fields': ('title', 'slug', 'body')}),
        ('SEO', {'fields': ('seo_title', 'seo_description')}),
        ('Публикация', {'fields': ('is_published', 'show_in_nav', 'show_in_footer', 'sort_order')}),
        ('Служебное', {'fields': ('created_at', 'updated_at')}),
    )
