import os
import django
from django.conf import settings

# Minimal Django settings to run standalone
if not settings.configured:
    settings.configure(
        INSTALLED_APPS=[
            'django.contrib.contenttypes',
            'django.contrib.auth',
            'rest_framework',
            'marketplace',
        ],
        SECRET_KEY='test',
    )
    django.setup()

from rest_framework.test import APIRequestFactory
from marketplace.interface.views import (
    UsuarioView, 
    CategoriaView, 
    PublicarProductoView,
    _usuario_repo,
    _categoria_repo,
    _producto_repo
)

def test_flow():
    factory = APIRequestFactory()
    
    print("--- 1. Creating User ---")
    usuario_data = {
        "id": "u-test-1",
        "nombre": "Juan Perez",
        "email": "juan@test.com",
        "telefono": "3001234567",
        "apartamento": "101"
    }
    request = factory.post('/usuarios/', usuario_data, format='json')
    view = UsuarioView.as_view()
    response = view(request)
    print(f"Status: {response.status_code}")
    print(f"Data: {response.data}")
    assert response.status_code == 201

    print("\n--- 2. Creating Category ---")
    categoria_data = {
        "id": "c-elec",
        "nombre": "Electronica",
        "descripcion": "Gadgets"
    }
    request = factory.post('/categorias/', categoria_data, format='json')
    view = CategoriaView.as_view()
    response = view(request)
    print(f"Status: {response.status_code}")
    print(f"Data: {response.data}")
    assert response.status_code == 201

    print("\n--- 1.1 Creating Duplicate User (Conflict) ---")
    request = factory.post('/usuarios/', usuario_data, format='json')
    view = UsuarioView.as_view()
    response = view(request)
    print(f"Status: {response.status_code}")
    print(f"Data: {response.data}")
    assert response.status_code == 409

    print("\n--- 3. Publishing Product (Success) ---")
    producto_data = {
        "vendedor_id": "u-test-1",
        "vendedor_status": "APPROVED",
        "nombre": "Laptop Gamer",
        "descripcion": " laptop muy rapida para jugar",
        "precio": 5000000,
        "categoria_id": "c-elec",
        "imagenes": ["http://img.com/1.jpg"]
    }
    request = factory.post('/publicar-producto/', producto_data, format='json')
    view = PublicarProductoView.as_view()
    response = view(request)
    print(f"Status: {response.status_code}")
    if hasattr(response, 'data'):
        print(f"Data: {response.data}")
    assert response.status_code == 201
    assert response.data['nombre'] == "Laptop Gamer"

    print("\n--- 4. Publishing Product (Fail - Invalid Price) ---")
    bad_data = producto_data.copy()
    bad_data['precio'] = 500 # Too low
    request = factory.post('/publicar-producto/', bad_data, format='json')
    view = PublicarProductoView.as_view()
    response = view(request)
    print(f"Status: {response.status_code}")
    print(f"Data: {response.data}")
    assert response.status_code == 400

    print("\n--- 5. Publishing Product (Fail - User Not Found) ---")
    bad_user_data = producto_data.copy()
    bad_user_data['vendedor_id'] = "u-ghost"
    request = factory.post('/publicar-producto/', bad_user_data, format='json')
    view = PublicarProductoView.as_view()
    response = view(request)
    print(f"Status: {response.status_code}")
    print(f"Data: {response.data}")
    # We implemented 404 for missing user/category
    assert response.status_code == 404

    print("\n[SUCCESS] All tests passed.")

if __name__ == "__main__":
    try:
        test_flow()
    except AssertionError as e:
        print(f"\n[FAILED] Assertion Error")
        exit(1)
    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()
        exit(1)
