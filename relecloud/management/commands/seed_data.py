from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from relecloud.models import Destination, Cruise, InfoRequest
from datetime import date

class Command(BaseCommand):
    help = 'Carga datos iniciales obligatorios para ISW2 (3 destinos con Station-9101460, 2 cruceros, 1 info request y superuser)'

    def handle(self, *args, **options):
        User = get_user_model()
        if not User.objects.filter(username='d4r1').exists():
            User.objects.create_superuser('d4r1', '9101460@alumnos.ufv.es', 'admin123456')
            self.stdout.write(self.style.SUCCESS('Superuser d4r1 creado con éxito.'))
        else:
            self.stdout.write('Superuser d4r1 ya existía.')

        # Destinos obligatorios
        dest1, _ = Destination.objects.get_or_create(
            name='Station-9101460',
            defaults={
                'latitude': 28.5721,
                'longitude': -80.6480,
                'description': 'Estación orbital de investigación y turismo espacial de Darío Rodríguez Pajares (Exp: 9101460).'
            }
        )

        dest2, _ = Destination.objects.get_or_create(
            name='Moon Base Alpha',
            defaults={
                'latitude': 0.6740,
                'longitude': 23.4720,
                'description': 'Lujoso resort lunar con vistas inigualables a la Tierra y paseos en gravedad reducida.'
            }
        )

        dest3, _ = Destination.objects.get_or_create(
            name='Mars Colony One',
            defaults={
                'latitude': -4.5895,
                'longitude': 137.4417,
                'description': 'Aventura en la primera colonia marciana. Exploración del cráter Gale y cañones marcianos.'
            }
        )

        # Cruceros
        cruise1, _ = Cruise.objects.get_or_create(
            name='Apollo Explorer',
            defaults={
                'description': 'Crucero orbital con escala en la estación y órbita lunar.',
                'departure_date': date(2026, 11, 1),
                'return_date': date(2026, 11, 15),
            }
        )
        cruise1.destinations.set([dest1, dest2])

        cruise2, _ = Cruise.objects.get_or_create(
            name='Ares Odyssey',
            defaults={
                'description': 'Expedición interplanetaria de lujo hacia la colonia roja.',
                'departure_date': date(2027, 1, 10),
                'return_date': date(2027, 3, 20),
            }
        )
        cruise2.destinations.set([dest1, dest3])

        # Solicitud de información de prueba
        if not InfoRequest.objects.filter(email='9101460@alumnos.ufv.es').exists():
            InfoRequest.objects.create(
                name='Darío Rodríguez Pajares',
                email='9101460@alumnos.ufv.es',
                cruise=cruise1,
                notes='Solicito información detallada sobre el embarque en Station-9101460.'
            )
            self.stdout.write(self.style.SUCCESS('InfoRequest de prueba creada.'))

        self.stdout.write(self.style.SUCCESS('Datos iniciales cargados correctamente (3 destinos, 2 cruceros).'))
