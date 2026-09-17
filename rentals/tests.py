from datetime import date
from decimal import Decimal

from django.contrib.auth.models import User
from django.contrib.staticfiles import finders
from django.test import TestCase
from django.urls import reverse

from rentals.models import Bike, Rental


class RentalFrontendTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username='anna', first_name='Anna', last_name='Nowak')
        cls.bike = Bike.objects.create(
            name='City Explorer', manufacturer='Romet', production_year=2025,
            purchase_date=date(2025, 3, 10), serial_number='RM-001',
            price_per_day=Decimal('45.00'),
        )
        cls.rental = Rental.objects.create(
            bike=cls.bike, user=cls.user, rental_date=date(2026, 9, 10),
        )

    def test_all_four_views_render_and_link_to_related_pages(self):
        pages = [
            ('rentals', [], 'rental_list.html', reverse('rental-detail', args=[self.rental.pk])),
            ('rental-detail', [self.rental.pk], 'rental_detail.html', reverse('bike-detail', args=[self.bike.pk])),
            ('bikes', [], 'bike_list.html', reverse('bike-detail', args=[self.bike.pk])),
            ('bike-detail', [self.bike.pk], 'bike_detail.html', reverse('bikes')),
        ]
        for name, args, template, linked_url in pages:
            with self.subTest(view=name):
                response = self.client.get(reverse(name, args=args))
                self.assertEqual(response.status_code, 200)
                self.assertTemplateUsed(response, template)
                self.assertContains(response, self.bike.name)
                self.assertContains(response, f'href="{linked_url}"')
                self.assertContains(response, '/static/rentals/css/main.css')

    def test_empty_lists(self):
        Rental.objects.all().delete()
        Bike.objects.all().delete()
        self.assertContains(self.client.get(reverse('rentals')), 'Pierwsza trasa jeszcze przed nami')
        self.assertContains(self.client.get(reverse('bikes')), 'Flota czeka na pierwszy rower')

    def test_open_rental_has_status_and_no_missing_date(self):
        response = self.client.get(reverse('rental-detail', args=[self.rental.pk]))
        self.assertContains(response, 'W trakcie')
        self.assertContains(response, 'Rower w trasie')
        self.assertContains(response, '10.09.2026')
        self.assertContains(response, 'Anna Nowak')
        self.assertNotContains(response, 'None')

    def test_returned_rental_displays_return_date_in_both_views(self):
        self.rental.return_date = date(2026, 9, 12)
        self.rental.save()
        for url in [reverse('rentals'), reverse('rental-detail', args=[self.rental.pk])]:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertContains(response, 'Zakończone')
                self.assertContains(response, '12.09.2026')

    def test_username_is_used_when_full_name_is_empty(self):
        self.user.first_name = self.user.last_name = ''
        self.user.save()
        self.assertContains(self.client.get(reverse('rentals')), '<td>anna</td>', html=True)

    def test_unknown_details_return_404(self):
        for name in ['bike-detail', 'rental-detail']:
            with self.subTest(view=name):
                self.assertEqual(self.client.get(reverse(name, args=[99999])).status_code, 404)

    def test_model_text_is_escaped(self):
        self.bike.name = '<script>alert(1)</script>'
        self.bike.save()
        for url in [reverse('bikes'), reverse('bike-detail', args=[self.bike.pk])]:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertContains(response, '&lt;script&gt;alert(1)&lt;/script&gt;')
                self.assertNotContains(response, self.bike.name)

    def test_stylesheet_is_discoverable(self):
        self.assertIsNotNone(finders.find('rentals/css/main.css'))

    def test_create_and_update_forms_render(self):
        for kind, instance in [('bike', self.bike), ('rental', self.rental)]:
            for action, args in [('create', []), ('update', [instance.pk])]:
                with self.subTest(kind=kind, action=action):
                    response = self.client.get(reverse(f'{kind}-{action}', args=args))
                    self.assertEqual(response.status_code, 200)
                    self.assertTemplateUsed(response, f'{kind}_form.html')
                    self.assertContains(response, 'csrfmiddlewaretoken')
                    self.assertContains(response, 'type="date"')
                    self.assertContains(response, 'Anuluj')
                    self.assertContains(response, 'aria-current="true"')
        response = self.client.get(reverse('bike-update', args=[self.bike.pk]))
        self.assertContains(response, 'value="2025-03-10"')
        self.assertContains(response, 'value="City Explorer"')

    def test_bike_create_and_update_save_and_redirect(self):
        data = {'name': 'Nowy rower', 'manufacturer': 'Romet',
                'production_year': 2025, 'purchase_date': '2025-03-10',
                'serial_number': 'RM-002', 'price_per_day': '60.50', 'is_active': 'on'}
        response = self.client.post(reverse('bike-create'), data)
        bike = Bike.objects.get(serial_number='RM-002')
        self.assertRedirects(response, reverse('bike-detail', args=[bike.pk]))
        data['name'] = 'Zmieniony rower'
        del data['is_active']
        response = self.client.post(reverse('bike-update', args=[bike.pk]), data)
        self.assertRedirects(response, reverse('bike-detail', args=[bike.pk]))
        bike.refresh_from_db()
        self.assertEqual(bike.name, 'Zmieniony rower')
        self.assertEqual(bike.price_per_day, Decimal('60.50'))
        self.assertFalse(bike.is_active)

    def test_rental_create_and_register_return(self):
        data = {'bike': self.bike.pk, 'user': self.user.pk,
                'rental_date': '2026-09-15', 'return_date': ''}
        response = self.client.post(reverse('rental-create'), data)
        rental = Rental.objects.exclude(pk=self.rental.pk).get()
        self.assertRedirects(response, reverse('rental-detail', args=[rental.pk]))
        self.assertIsNone(rental.return_date)
        data['return_date'] = '2026-09-17'
        response = self.client.post(reverse('rental-update', args=[rental.pk]), data)
        self.assertRedirects(response, reverse('rental-detail', args=[rental.pk]))
        rental.refresh_from_db()
        self.assertEqual(rental.return_date, date(2026, 9, 17))

    def test_invalid_forms_preserve_input_and_do_not_save(self):
        for kind, model in [('bike', Bike), ('rental', Rental)]:
            count = model.objects.count()
            response = self.client.post(reverse(f'{kind}-create'), {})
            self.assertContains(response, 'Sprawdź zaznaczone pola')
            self.assertContains(response, 'To pole jest wymagane.')
            self.assertEqual(model.objects.count(), count)
        response = self.client.post(reverse('rental-update', args=[self.rental.pk]), {
            'bike': self.bike.pk, 'user': self.user.pk,
            'rental_date': '2026-09-10', 'return_date': '2026-09-09',
        })
        self.assertContains(response, 'Data zwrotu nie może być wcześniejsza')
        self.assertContains(response, 'value="2026-09-09"')
        self.rental.refresh_from_db()
        self.assertIsNone(self.rental.return_date)

    def test_creation_and_edit_links_are_available(self):
        for kind, list_name, instance in [('bike', 'bikes', self.bike), ('rental', 'rentals', self.rental)]:
            self.assertContains(self.client.get(reverse(list_name)),
                                f'href="{reverse(kind + "-create")}"')
            self.assertContains(self.client.get(reverse(kind + '-detail', args=[instance.pk])),
                                f'href="{reverse(kind + "-update", args=[instance.pk])}"')
