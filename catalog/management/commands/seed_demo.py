from django.core.management.base import BaseCommand

from catalog.models import Category, Person, SiteSettings, StaticPage, TextBlock


class Command(BaseCommand):
    help = 'Заполняет проект демонстрационными данными.'

    def handle(self, *args, **options):
        SiteSettings.objects.update_or_create(
            pk=1,
            defaults={
                'site_name': 'MineCatalog',
                'site_tagline': 'Пиксельный каталог персоналий',
                'default_seo_title': 'MineCatalog — редакционный каталог',
                'default_seo_description': 'Гибкий каталог персоналий с категориями, пояснениями и источниками.',
                'footer_text': 'Все материалы публикуются в редакционных целях.',
                'contacts_email': 'admin@example.com',
                'contacts_telegram': '@minecatalog',
                'copyright_text': '© MineCatalog',
            },
        )

        blocks = [
            (
                'home_intro',
                'Текст над списком на главной',
                'Это демонстрационный текст. Его можно изменить в админке без правки кода.',
            ),
            (
                'home_bottom_text',
                'Текст под списком на главной',
                'Здесь можно разместить пояснение, дисклеймер или дополнительный редакционный комментарий.',
            ),
            (
                'contacts_note',
                'Заметка для страницы контактов',
                'Для связи используйте email или Telegram, указанные в настройках сайта.',
            ),
        ]
        for key, title, content in blocks:
            TextBlock.objects.update_or_create(
                key=key,
                defaults={'title': title, 'content': content, 'is_active': True},
            )

        categories = [
            {
                'title': 'Основная категория',
                'short_description': 'Основная демонстрационная категория.',
                'description': 'Подробное описание основной категории. Текст редактируется в админке.',
                'sort_order': 1,
            },
            {
                'title': 'Спорная категория',
                'short_description': 'Категория для спорных и обсуждаемых случаев.',
                'description': 'Здесь можно описать критерии, по которым записи попадают в эту категорию.',
                'sort_order': 2,
            },
            {
                'title': 'Редакционная оценка',
                'short_description': 'Категория для редакционных материалов.',
                'description': 'Эта категория помогает отделять факты от редакционных оценок.',
                'sort_order': 3,
            },
        ]

        created_categories = {}
        for item in categories:
            category, _ = Category.objects.update_or_create(
                title=item['title'],
                defaults=item,
            )
            created_categories[item['title']] = category

        pages = [
            {
                'title': 'О сайте',
                'body': 'Это пример статической страницы. Здесь можно рассказать о проекте, методологии и критериях отбора.',
                'show_in_nav': True,
                'show_in_footer': True,
                'sort_order': 1,
            },
            {
                'title': 'Контакты',
                'body': 'На этой странице можно разместить контактную информацию, форму связи или реквизиты.',
                'show_in_nav': True,
                'show_in_footer': True,
                'sort_order': 2,
            },
            {
                'title': 'Политика конфиденциальности',
                'body': 'Короткий текст политики конфиденциальности для MVP. При необходимости замените на свою версию.',
                'show_in_nav': False,
                'show_in_footer': True,
                'sort_order': 10,
            },
        ]

        for page in pages:
            StaticPage.objects.update_or_create(title=page['title'], defaults=page)

        persons = [
            {
                'name': 'Тестовая запись №1',
                'category': created_categories['Основная категория'],
                'status_label': 'подтверждено',
                'short_caption': 'Короткая подпись для первой записи.',
                'description': 'Подробное описание карточки. Здесь можно изложить основную информацию.',
                'reasoning': 'Здесь объясняется, почему запись относится к выбранной категории.',
                'extra_information': 'Дополнительные сведения, которые не вошли в основной текст.',
                'sources_notes': 'Источник 1\nИсточник 2\nПримечание редакции',
                'editorial_note': 'Информация носит редакционный характер.',
                'sort_order': 1,
            },
            {
                'name': 'Тестовая запись №2',
                'category': created_categories['Спорная категория'],
                'status_label': 'спорно',
                'short_caption': 'Короткая подпись для второй записи.',
                'description': 'Основной текст для второй карточки.',
                'reasoning': 'Обоснование решения по второй карточке.',
                'extra_information': 'Дополнительный блок сведений.',
                'sources_notes': 'Список источников и примечаний.',
                'editorial_note': 'Требует дополнительной проверки.',
                'sort_order': 2,
            },
            {
                'name': 'Тестовая запись №3',
                'category': created_categories['Редакционная оценка'],
                'status_label': 'редакционно',
                'short_caption': 'Третья демонстрационная карточка.',
                'description': 'Описание третьей карточки.',
                'reasoning': 'Аргументация и логика отнесения к категории.',
                'extra_information': 'Еще один дополнительный блок.',
                'sources_notes': 'Источники и редакционные пояснения.',
                'editorial_note': 'Материал содержит оценочные суждения.',
                'sort_order': 3,
            },
        ]

        for item in persons:
            Person.objects.update_or_create(
                name=item['name'],
                defaults={**item, 'is_published': True, 'show_on_homepage': True},
            )

        self.stdout.write(self.style.SUCCESS('Демонстрационные данные успешно добавлены.'))
