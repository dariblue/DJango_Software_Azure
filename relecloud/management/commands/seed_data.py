from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from relecloud.models import Destination, Cruise, InfoRequest
from datetime import date

class Command(BaseCommand):
    help = 'Carga datos iniciales obligatorios para ISW2 con descripciones breves'

    def handle(self, *args, **options):
        User = get_user_model()
        if not User.objects.filter(username='d4r1').exists():
            User.objects.create_superuser('d4r1', '9101460@alumnos.ufv.es', 'admin123456')
            self.stdout.write(self.style.SUCCESS('Superuser d4r1 creado con éxito.'))
        else:
            self.stdout.write('Superuser d4r1 ya existía.')

        # 1. Destino obligatorio Canvas
        dest1, _ = Destination.objects.update_or_create(
            name='Station-9101460',
            defaults={
                'latitude': 28.5721,
                'longitude': -80.6480,
                'description': 'Estacion orbital de Dario Rodriguez (Exp: 9101460). Vistas increibles a la Tierra y parada para repostar.'
            }
        )

        # 2. Exoplaneta habitable a tomar por saco
        dest2, _ = Destination.objects.update_or_create(
            name='Kepler-452b (Tierra 2.0)',
            defaults={
                'latitude': 44.2738,
                'longitude': 112.5930,
                'description': 'La Tierra 2.0 a 1.400 años luz. Es habitable pero el viaje se hace un poco largo.'
            }
        )

        # 3. Luna helada con oceano
        dest3, _ = Destination.objects.update_or_create(
            name='Europa (Oceano Bajo Hielo)',
            defaults={
                'latitude': -9.6200,
                'longitude': 45.1300,
                'description': 'Luna helada de Jupiter con oceano subterraneo. Traete abrigo porque el agua esta helada.'
            }
        )

        # Cruceros
        cruise1, _ = Cruise.objects.update_or_create(
            name='Ruta Orbital Transiberica',
            defaults={
                'description': 'Viaje rapido con escala en Station-9101460 y destino en Europa.',
                'departure_date': date(2026, 11, 1),
                'return_date': date(2026, 11, 15),
            }
        )
        cruise1.destinations.set([dest1, dest3])

        cruise2, _ = Cruise.objects.update_or_create(
            name='Expedicion Sin Retorno a Kepler',
            defaults={
                'description': 'Viaje directo en camaras de criogenizacion hacia la Tierra 2.0.',
                'departure_date': date(2027, 1, 10),
                'return_date': date(2027, 3, 20),
            }
        )
        cruise2.destinations.set([dest1, dest2])

        # Solicitud de información de prueba
        if not InfoRequest.objects.filter(email='9101460@alumnos.ufv.es').exists():
            InfoRequest.objects.create(
                name='Darío Rodríguez Pajares',
                email='9101460@alumnos.ufv.es',
                cruise=cruise2,
                notes='¿Hay wifi en las camaras de criogenizacion para Kepler?'
            )
            self.stdout.write(self.style.SUCCESS('InfoRequest de prueba creada.'))

        self.stdout.write(self.style.SUCCESS('Datos iniciales cargados con descripciones cortas.'))
