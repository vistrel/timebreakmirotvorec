from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator, RegexValidator
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


def validate_image_size(image):
    max_size = 5 * 1024 * 1024
    if image.size > max_size:
        raise ValidationError('Изображение слишком большое. Максимум: 5 МБ.')


class SiteSettings(models.Model):
    site_name = models.CharField('Название сайта', max_length=120, default='MineCatalog')
    site_tagline = models.CharField('Подзаголовок сайта', max_length=220, blank=True)
    default_seo_title = models.CharField('SEO title по умолчанию', max_length=180, blank=True)
    default_seo_description = models.CharField('SEO description по умолчанию', max_length=255, blank=True)
    footer_text = models.TextField('Текст в футере', blank=True)
    contacts_email = models.EmailField('Контактный email', blank=True)
    contacts_telegram = models.CharField('Telegram', max_length=120, blank=True)
    copyright_text = models.CharField('Копирайт', max_length=220, blank=True)
    updated_at = models.DateTimeField('Обновлено', auto_now=True)

    class Meta:
        verbose_name = 'Настройки сайта'
        verbose_name_plural = 'Настройки сайта'

    def __str__(self):
        return 'Основные настройки сайта'

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)


class TextBlock(models.Model):
    key = models.CharField(
        'Ключ',
        max_length=50,
        unique=True,
        help_text='Например: home_intro, home_bottom_text, contacts_note',
        validators=[
            RegexValidator(
                regex=r'^[a-z0-9_]+$',
                message='Используйте только строчные латинские буквы, цифры и _.',
            )
        ],
    )
    title = models.CharField('Название блока', max_length=120)
    content = models.TextField('Содержимое', blank=True)
    is_active = models.BooleanField('Активен', default=True)
    updated_at = models.DateTimeField('Обновлено', auto_now=True)

    class Meta:
        verbose_name = 'Текстовый блок'
        verbose_name_plural = 'Текстовые блоки'
        ordering = ['title']

    def __str__(self):
        return f'{self.title} ({self.key})'


class Category(models.Model):
    title = models.CharField('Название категории', max_length=120, unique=True)
    slug = models.SlugField('Slug', max_length=140, unique=True, blank=True, allow_unicode=True)
    short_description = models.CharField('Короткое описание', max_length=180, blank=True)
    description = models.TextField('Полное описание категории', blank=True)
    seo_title = models.CharField('SEO title', max_length=180, blank=True)
    seo_description = models.CharField('SEO description', max_length=255, blank=True)
    sort_order = models.PositiveIntegerField('Порядок сортировки', default=0)
    is_active = models.BooleanField('Показывать категорию', default=True)
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлено', auto_now=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['sort_order', 'title']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})


class Person(models.Model):
    name = models.CharField('Имя / название', max_length=150)
    slug = models.SlugField('Slug', max_length=160, unique=True, blank=True, allow_unicode=True)
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        related_name='persons',
        on_delete=models.PROTECT,
    )
    status_label = models.CharField(
        'Статус / метка',
        max_length=80,
        blank=True,
        help_text='Например: подтверждено, спорно, редакционная оценка',
    )
    short_caption = models.CharField('Короткая подпись', max_length=220, blank=True)
    image = models.ImageField(
        'Изображение',
        upload_to='people/%Y/%m/',
        blank=True,
        validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp']),
            validate_image_size,
        ],
    )
    description = models.TextField('Основное описание', blank=True)
    reasoning = models.TextField('Почему мы так считаем', blank=True)
    extra_information = models.TextField('Дополнительная информация', blank=True)
    sources_notes = models.TextField('Источники / примечания', blank=True)
    editorial_note = models.TextField(
        'Редакционное примечание',
        blank=True,
        help_text='Например: информация носит оценочный/редакционный характер.',
    )
    seo_title = models.CharField('SEO title', max_length=180, blank=True)
    seo_description = models.CharField('SEO description', max_length=255, blank=True)
    is_published = models.BooleanField('Опубликовано', default=True)
    show_on_homepage = models.BooleanField('Показывать на главной', default=True)
    sort_order = models.PositiveIntegerField('Порядок сортировки', default=0)
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлено', auto_now=True)

    class Meta:
        verbose_name = 'Карточка'
        verbose_name_plural = 'Карточки'
        ordering = ['sort_order', 'name']
        indexes = [
            models.Index(fields=['is_published', 'show_on_homepage']),
            models.Index(fields=['slug']),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('person_detail', kwargs={'slug': self.slug})


class StaticPage(models.Model):
    title = models.CharField('Заголовок', max_length=140)
    slug = models.SlugField('Slug', max_length=160, unique=True, blank=True, allow_unicode=True)
    body = models.TextField('Содержимое', blank=True)
    seo_title = models.CharField('SEO title', max_length=180, blank=True)
    seo_description = models.CharField('SEO description', max_length=255, blank=True)
    is_published = models.BooleanField('Опубликовано', default=True)
    show_in_nav = models.BooleanField('Показывать в верхнем меню', default=False)
    show_in_footer = models.BooleanField('Показывать в футере', default=True)
    sort_order = models.PositiveIntegerField('Порядок сортировки', default=0)
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлено', auto_now=True)

    class Meta:
        verbose_name = 'Статическая страница'
        verbose_name_plural = 'Статические страницы'
        ordering = ['sort_order', 'title']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('static_page', kwargs={'slug': self.slug})
