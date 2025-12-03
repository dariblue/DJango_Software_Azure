from django.core import mail
from django.test import TestCase
from django.urls import reverse
from datetime import date

from .models import Cruise, Destination

class InfoRequestEmailTest(TestCase):

    def setUp(self):
        # Crear destino mínimo
        self.destination = Destination.objects.create(
            name="Paris",
            description="Destino de prueba",
            latitude=0,
            longitude=0
        )

        # Crear crucero válido
        self.cruise = Cruise.objects.create(
            name="Crucero Test",
            description="Crucero de prueba",
            departure_date=date.today(),
            return_date=date.today()
        )

        self.cruise.destinations.add(self.destination)

    def test_info_request_envia_email(self):
        post_data = {
            'name': 'Juan Perez',
            'email': 'juan@example.com',
            'notes': 'Quiero información',
            'cruise': self.cruise.pk
        }

        response = self.client.post(reverse('info_request'), data=post_data)

        self.assertEqual(len(mail.outbox), 1)

        email = mail.outbox[0]
        self.assertIn("Juan Perez", email.body)
        self.assertIn("Crucero Test", email.body)
        self.assertIn("juan@example.com", email.body)


