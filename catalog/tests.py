from django.test import TestCase
from django.urls import reverse

from .models import Category, Person, SiteSettings, StaticPage


class CatalogViewsTests(TestCase):
    def setUp(self):
        SiteSettings.objects.create(
            site_name='Test Catalog',
            default_seo_title='Test Catalog',
            default_seo_description='Test description',
        )
        self.category = Category.objects.create(title='Герои')
        self.person = Person.objects.create(
            name='Тестовый персонаж',
            category=self.category,
            short_caption='Краткая подпись',
            description='Описание',
            is_published=True,
            show_on_homepage=True,
        )
        self.page = StaticPage.objects.create(title='О сайте', body='Текст страницы')

    def test_home_page_loads(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.person.name)

    def test_person_detail_loads(self):
        response = self.client.get(reverse('person_detail', kwargs={'slug': self.person.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.person.name)

    def test_static_page_loads(self):
        response = self.client.get(reverse('static_page', kwargs={'slug': self.page.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.page.title)
