"""
Script para probar el sistema de emails
Ejecutar con: python test_emails.py
"""
import requests
import json
import time

BASE_URL = "http://localhost:8000/api/v1"

def print_section(title):
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60 + "\n")

def test_welcome_email():
    """Test 1: Email de bienvenida al registrarse"""
    print_section("TEST 1: Email de Bienvenida (Registro)")

    # Generar email único con timestamp
    import random
    email = f"test{random.randint(1000, 9999)}@example.com"

    data = {
        "email": email,
        "password": "password123",
        "full_name": "Usuario de Prueba"
    }

    print(f"[*] Registrando usuario: {email}")
    response = requests.post(f"{BASE_URL}/auth/register", json=data)

    if response.status_code == 201:
        print("[OK] Usuario registrado exitosamente!")
        print(f"[EMAIL] Deberias recibir un email de bienvenida en: {email}")
        print(f"[INFO] Revisa tu Gmail: {data['email']}")
        return email
    else:
        print(f"[ERROR] Error: {response.status_code}")
        print(response.json())
        return None

def test_password_reset(email):
    """Test 2: Email de recuperación de contraseña"""
    print_section("TEST 2: Email de Recuperación de Contraseña")

    if not email:
        email = input("Ingresa un email registrado: ")

    data = {"email": email}

    print(f"[*] Solicitando reset de contrasena para: {email}")
    response = requests.post(f"{BASE_URL}/auth/password-reset/request", json=data)

    if response.status_code == 200:
        print("[OK] Solicitud enviada exitosamente!")
        print(f"[EMAIL] Deberias recibir un email con el link de recuperacion")
        print(f"[INFO] Revisa tu Gmail: {email}")
        print("\n[WARNING] El link expira en 30 minutos")
        return True
    else:
        print(f"[ERROR] Error: {response.status_code}")
        print(response.json())
        return False

def test_order_confirmation():
    """Test 3: Email de confirmación de pedido"""
    print_section("TEST 3: Email de Confirmacion de Pedido")

    print("[WARNING] Para probar el email de confirmacion de pedido necesitas:")
    print("   1. Tener un usuario autenticado")
    print("   2. Agregar productos al carrito")
    print("   3. Crear el pedido")
    print("\n   Esto es mas complejo, te recomiendo probarlo desde el frontend")
    print("   o manualmente con Postman/Thunder Client\n")

def main():
    print("\n" + "="*60)
    print("  PRUEBA DE SISTEMA DE EMAILS - TIENDA ASIATICA")
    print("="*60)

    print("\nEmail configurado: azambranozarallo@gmail.com")
    print("IMPORTANTE: Revisa tu carpeta de SPAM si no ves los emails\n")

    try:
        # Test 1: Welcome Email
        email = test_welcome_email()

        if email:
            time.sleep(2)  # Pequeña pausa

            # Test 2: Password Reset
            test_password_reset(email)

        time.sleep(2)

        # Test 3: Order Confirmation (info only)
        test_order_confirmation()

        print("\n" + "="*60)
        print("  RESUMEN")
        print("="*60)
        print("\n[OK] Tests completados!")
        print("\n[INFO] Revisa tu Gmail: azambranozarallo@gmail.com")
        print("   - Email de bienvenida")
        print("   - Email de recuperacion de contrasena")
        print("\n[WARNING] Si no ves los emails:")
        print("   1. Revisa la carpeta de SPAM")
        print("   2. Busca por 'Tienda Alimentacion Asiatica'")
        print("   3. Espera 1-2 minutos (puede tardar)")

    except requests.exceptions.ConnectionError:
        print("\n[ERROR] Error: No se puede conectar al backend")
        print("   Asegurate de que el backend este corriendo en http://localhost:8000")
    except Exception as e:
        print(f"\n[ERROR] Error inesperado: {e}")

if __name__ == "__main__":
    main()
