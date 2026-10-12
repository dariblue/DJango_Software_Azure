import os
import sys
from pathlib import Path

# Add project root to sys.path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

# Configure environment for production rehearsal
os.environ['DJANGO_SETTINGS_MODULE'] = 'project.settings'
os.environ['DEBUG'] = 'False'
os.environ['ALLOWED_HOSTS'] = 'localhost,127.0.0.1,testserver'

import django
django.setup()

from django.test import Client

client = Client()

print("=== INICIANDO ENSAYO LOCAL DE PRODUCCIÓN (DEBUG=False, WhiteNoise) ===")

from relecloud.models import Destination
station = Destination.objects.filter(name__startswith='Station').first() or Destination.objects.first()
pk = station.pk if station else 1

checks = [
    ('/', 200, 'Home page'),
    ('/about/', 200, 'About page with student ID'),
    ('/destinations/', 200, 'Destinations list'),
    (f'/destination/{pk}/', 200, f'Destination detail ({station.name if station else "Station"})'),
    ('/destination/add/', 200, 'Destination add form'),
    (f'/destination/{pk}/update/', 200, 'Destination update form'),
    (f'/destination/{pk}/delete/', 200, 'Destination delete confirmation'),
    ('/info_request/', 200, 'Info request form'),
    ('/nonexistent-test-404/', 404, 'Clean 404 page'),
]

all_passed = True
for url, expected_status, description in checks:
    response = client.get(url)
    status_ok = response.status_code == expected_status
    if not status_ok:
        all_passed = False
    print(f"[{'PASS' if status_ok else 'FAIL'}] {description} ({url}) -> Status: {response.status_code} (Esperado: {expected_status})")

# Test student info in about page
res_about = client.get('/about/')
content_about = res_about.content.decode('utf-8')
if 'id="student-name"' in content_about and 'Darío Rodríguez Pajares' in content_about:
    print("[PASS] #student-name presente con 'Darío Rodríguez Pajares'")
else:
    print("[FAIL] #student-name no encontrado o incorrecto")
    all_passed = False

if 'id="student-id"' in content_about and '9101460' in content_about:
    print("[PASS] #student-id presente con '9101460'")
else:
    print("[FAIL] #student-id no encontrado o incorrecto")
    all_passed = False

if all_passed:
    print("\n✅ TODOS LOS CHECKS DE PRODUCCIÓN EN LOCAL HAN PASADO SATISFACTORIAMENTE.")
    sys.exit(0)
else:
    print("\n❌ HUBO ERRORES EN EL ENSAYO DE PRODUCCIÓN.")
    sys.exit(1)
