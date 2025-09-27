import requests
import json
import sys
import os
from getpass import getpass

class ClienteTareas:
    def __init__(self, base_url="http://127.0.0.1:5000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.usuario_actual = None
        self.usuario_id = None
    
    def limpiar_pantalla(self):
  
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def mostrar_menu_principal(self):
     
        self.limpiar_pantalla()
        print("=" * 50)
        print("    SISTEMA DE GESTIÓN DE TAREAS")
        print("=" * 50)
        print("1. Registrarse")
        print("2. Iniciar sesión")
        print("3. Salir")
        print("=" * 50)
    
    def mostrar_menu_usuario(self):
   
        self.limpiar_pantalla()
        print("=" * 50)
        print(f"    BIENVENIDO: {self.usuario_actual}")
        print("=" * 50)
        print("1. Ver página de bienvenida")
        print("2. Cerrar sesión")
        print("3. Salir")
        print("=" * 50)
    
    def registrar_usuario(self):
     
        print("\n--- REGISTRO DE USUARIO ---")
        usuario = input("Usuario: ").strip()
        if not usuario:
            print(" El usuario no puede estar vacío")
            input("Presiona Enter para continuar...")
            return
        
        contraseña = getpass("Contraseña: ")
        if not contraseña:
            print(" La contraseña no puede estar vacía")
            input("Presiona Enter para continuar...")
            return
        
        try:
            data = {
                "usuario": usuario,
                "contraseña": contraseña
            }
            
            response = self.session.post(
                f"{self.base_url}/registro",
                json=data,
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 201:
                print(" Usuario registrado correctamente")
            else:
                error_data = response.json()
                print(f" Error: {error_data.get('error', 'Error desconocido')}")
            
        except requests.exceptions.ConnectionError:
            print(" Error: No se puede conectar al servidor")
            print("   Asegúrate de que el servidor esté ejecutándose")
        except Exception as e:
            print(f" Error inesperado: {e}")
        
        input("\nPresiona Enter para continuar...")
    
    def iniciar_sesion(self):
       
        print("\n--- INICIO DE SESIÓN ---")
        usuario = input("Usuario: ").strip()
        if not usuario:
            print(" El usuario no puede estar vacío")
            input("Presiona Enter para continuar...")
            return
        
        contraseña = getpass("Contraseña: ")
        if not contraseña:
            print(" La contraseña no puede estar vacía")
            input("Presiona Enter para continuar...")
            return
        
        try:
            data = {
                "usuario": usuario,
                "contraseña": contraseña
            }
            
            response = self.session.post(
                f"{self.base_url}/login",
                json=data,
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 200:
                response_data = response.json()
                self.usuario_actual = usuario
                self.usuario_id = response_data.get('usuario_id')
                print(" Inicio de sesión exitoso")
                input("Presiona Enter para continuar...")
                return True
            else:
                error_data = response.json()
                print(f" Error: {error_data.get('error', 'Error desconocido')}")
                
        except requests.exceptions.ConnectionError:
            print(" Error: No se puede conectar al servidor")
            print("   Asegúrate de que el servidor esté ejecutándose")
        except Exception as e:
            print(f" Error inesperado: {e}")
        
        input("\nPresiona Enter para continuar...")
        return False
    
    def ver_pagina_bienvenida(self):
     
        print("\n--- PÁGINA DE BIENVENIDA ---")
        try:
            response = self.session.get(f"{self.base_url}/tareas")
            
            if response.status_code == 200:
            
                html_content = response.text
                
                
                if '<div class="container">' in html_content:
                    start = html_content.find('<div class="container">')
                    end = html_content.find('</div>', start) + 6
                    content = html_content[start:end]
              
                    content = content.replace('<h1>', '\n# ').replace('</h1>', '')
                    content = content.replace('<h2>', '\n## ').replace('</h2>', '')
                    content = content.replace('<p>', '\n').replace('</p>', '')
                    content = content.replace('<li>', '\n• ').replace('</li>', '')
                    content = content.replace('<ul>', '').replace('</ul>', '')
                    content = content.replace('<strong>', '').replace('</strong>', '')
                    content = content.replace('<div class="container">', '').replace('</div>', '')
                    content = content.replace('<div class="info">', '').replace('</div>', '')
                    
                
                    content = '\n'.join(line.strip() for line in content.split('\n') if line.strip())
                    
                    print(content)
                else:
                    print("Contenido HTML recibido:")
                    print(response.text[:500] + "..." if len(response.text) > 500 else response.text)
            else:
                print(f" Error del servidor: {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            print(" Error: No se puede conectar al servidor")
            print("   Asegúrate de que el servidor esté ejecutándose")
        except Exception as e:
            print(f" Error inesperado: {e}")
        
        input("\nPresiona Enter para continuar...")
    
    def cerrar_sesion(self):
     
        self.usuario_actual = None
        self.usuario_id = None
        self.session = requests.Session()
        print("Sesión cerrada correctamente")
        input("Presiona Enter para continuar...")
    
    def ejecutar(self):
        
        while True:
            if self.usuario_actual:
                self.mostrar_menu_usuario()
                opcion = input("Selecciona una opción: ").strip()
                
                if opcion == "1":
                    self.ver_pagina_bienvenida()
                elif opcion == "2":
                    self.cerrar_sesion()
                elif opcion == "3":
                    print("¡Hasta luego!")
                    break
                else:
                    print("Opción no válida")
                    input("Presiona Enter para continuar...")
            else:
                self.mostrar_menu_principal()
                opcion = input("Selecciona una opción: ").strip()
                
                if opcion == "1":
                    self.registrar_usuario()
                elif opcion == "2":
                    if self.iniciar_sesion():
                        continue
                elif opcion == "3":
                    print("¡Hasta luego!")
                    break
                else:
                    print("Opción no válida")
                    input("Presiona Enter para continuar...")

def main():

    print("Iniciando cliente del Sistema de Gestión de Tareas...")
    
   
    try:
        response = requests.get("http://127.0.0.1:5000/tareas", timeout=5)
        print(" Servidor conectado correctamente")
    except:
        print(" ADVERTENCIA: No se puede conectar al servidor")
        print("   Asegúrate de ejecutar 'python servidor.py' en otra terminal")
        print("   El cliente continuará pero no podrá comunicarse con el servidor")
    
    input("Presiona Enter para continuar...")
 
    cliente = ClienteTareas()
    try:
        cliente.ejecutar()
    except KeyboardInterrupt:
        print("\n\n ¡Hasta luego!")
    except Exception as e:
        print(f"\n Error inesperado: {e}")

if __name__ == "__main__":
    main()
