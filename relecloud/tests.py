from django.test import TestCase, Client
from django.urls import reverse
from datetime import date
from relecloud.models import Destination, Cruise, InfoRequest

class RelecloudCanvasRequirementsTest(TestCase):
    def setUp(self):
        self.client = Client()
        # Create initial test data
        self.dest_station = Destination.objects.create(
            name='Station-9101460',
            latitude=28.5721,
            longitude=-80.6480,
            description='Estación orbital de Darío Rodríguez Pajares.'
        )
        self.dest_moon = Destination.objects.create(
            name='Moon Base Alpha',
            latitude=0.6740,
            longitude=23.4720,
            description='Resort lunar.'
        )
        self.dest_mars = Destination.objects.create(
            name='Mars Colony One',
            latitude=-4.5895,
            longitude=137.4417,
            description='Colonia marciana.'
        )

        self.cruise1 = Cruise.objects.create(
            name='Apollo Explorer',
            description='Crucero orbital.',
            departure_date=date(2026, 11, 1),
            return_date=date(2026, 11, 15)
        )
        self.cruise1.destinations.set([self.dest_station, self.dest_moon])

        self.cruise2 = Cruise.objects.create(
            name='Ares Odyssey',
            description='Crucero interplanetario.',
            departure_date=date(2027, 1, 10),
            return_date=date(2027, 3, 20)
        )
        self.cruise2.destinations.set([self.dest_station, self.dest_mars])

    def test_required_exact_routes_exist_and_return_200(self):
        """Verifica que todas las rutas exactas requeridas por Canvas responden 200."""
        routes = [
            '/',
            '/about/',
            '/destinations/',
            f'/destination/{self.dest_station.pk}/',
            '/destination/add/',
            f'/destination/{self.dest_station.pk}/update/',
            f'/destination/{self.dest_station.pk}/delete/',
            '/info_request/',
        ]
        for route in routes:
            response = self.client.get(route)
            self.assertEqual(
                response.status_code, 200,
                f"La ruta obligatoria '{route}' falló con código {response.status_code}"
            )

    def test_about_page_contains_student_name_and_id(self):
        """Verifica los elementos obligatorios #student-name y #student-id en /about/."""
        response = self.client.get('/about/')
        self.assertEqual(response.status_code, 200)
        content = response.content.decode('utf-8')
        self.assertIn('id="student-name"', content)
        self.assertIn('Darío Rodríguez Pajares', content)
        self.assertIn('id="student-id"', content)
        self.assertIn('9101460', content)

    def test_database_contains_station_9101460_and_cruises(self):
        """Verifica al menos 3 destinos (con Station-9101460) y 2 cruceros."""
        self.assertGreaterEqual(Destination.objects.count(), 3)
        self.assertTrue(Destination.objects.filter(name='Station-9101460').exists())
        self.assertGreaterEqual(Cruise.objects.count(), 2)

    def test_destination_crud_workflow(self):
        """Comprueba el ciclo CRUD completo de destinos: crear, editar y borrar."""
        # 1. Crear
        create_url = '/destination/add/'
        create_data = {
            'name': 'Venus Cloud City',
            'description': 'Estación flotante en la atmósfera de Venus.',
            'latitude': -12.34,
            'longitude': 56.78
        }
        res_create = self.client.post(create_url, create_data)
        self.assertEqual(res_create.status_code, 302)
        new_dest = Destination.objects.get(name='Venus Cloud City')

        # 2. Editar
        update_url = f'/destination/{new_dest.pk}/update/'
        update_data = {
            'name': 'Venus Cloud City Updated',
            'description': 'Descripción actualizada de Venus.',
            'latitude': -12.34,
            'longitude': 56.78
        }
        res_update = self.client.post(update_url, update_data)
        self.assertEqual(res_update.status_code, 302)
        new_dest.refresh_from_db()
        self.assertEqual(new_dest.name, 'Venus Cloud City Updated')

        # 3. Borrar
        delete_url = f'/destination/{new_dest.pk}/delete/'
        res_delete = self.client.post(delete_url)
        self.assertEqual(res_delete.status_code, 302)
        self.assertFalse(Destination.objects.filter(pk=new_dest.pk).exists())

    def test_info_request_create_and_redirect_to_index(self):
        """Comprueba que /info_request/ procesa la solicitud, la guarda y redirige a '/'."""
        initial_count = InfoRequest.objects.count()
        info_url = '/info_request/'
        post_data = {
            'name': 'Darío Rodríguez Pajares',
            'email': '9101460@alumnos.ufv.es',
            'cruise': self.cruise1.pk,
            'notes': 'Por favor envíenme detalles sobre el crucero Apollo Explorer.'
        }
        response = self.client.post(info_url, post_data)
        # Redirección a '/' (index)
        self.assertRedirects(response, '/', target_status_code=200)
        self.assertEqual(InfoRequest.objects.count(), initial_count + 1)
        created_req = InfoRequest.objects.latest('id')
        self.assertEqual(created_req.name, 'Darío Rodríguez Pajares')
        self.assertEqual(created_req.cruise, self.cruise1)

    def test_debug_false_clean_404_response(self):
        """Comprueba que con DEBUG=False una URL errónea devuelve 404 limpio sin traceback."""
        with self.settings(DEBUG=False):
            client = Client()
            response = client.get('/nonexistent-url-canvas-test/')
            self.assertEqual(response.status_code, 404)
            # No debe contener el trace de error de Django debug
            self.assertNotIn('Traceback (most recent call last)', response.content.decode('utf-8'))
