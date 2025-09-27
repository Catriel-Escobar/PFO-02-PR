from flask import Flask, request, jsonify, render_template
import sqlite3
import os
import time
from werkzeug.security import generate_password_hash, check_password_hash
from contextlib import contextmanager

app = Flask(__name__)

DB_PATH = 'tareas.db'

@contextmanager
def get_db_connection():
   
    conn = None
    max_retries = 3
    retry_delay = 0.1
    
    for attempt in range(max_retries):
        try:
            conn = sqlite3.connect(DB_PATH, timeout=10.0)
            conn.execute("PRAGMA journal_mode=WAL") 
            conn.execute("PRAGMA synchronous=NORMAL")  
            yield conn
            break
        except sqlite3.OperationalError as e:
            if "database is locked" in str(e) and attempt < max_retries - 1:
                time.sleep(retry_delay * (2 ** attempt))  
                continue
            else:
                raise
        finally:
            if conn:
                conn.close()

def init_db():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
        ''')
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS tareas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            descripcion TEXT,
            completada BOOLEAN DEFAULT 0,
            usuario_id INTEGER,
            FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
        )
        ''')
        
        conn.commit()

init_db()


@app.route('/registro', methods=['POST'])
def registro():
    data = request.get_json()
    
    if not data or 'usuario' not in data or 'contraseña' not in data:
        return jsonify({'error': 'Datos incompletos'}), 400
    
    usuario = data['usuario']
    contraseña = data['contraseña']
    
    hashed_password = generate_password_hash(contraseña)
    
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO usuarios (usuario, password) VALUES (?, ?)', 
                          (usuario, hashed_password))
            conn.commit()
        return jsonify({'mensaje': 'Usuario registrado correctamente'}), 201
    except sqlite3.IntegrityError:
        return jsonify({'error': 'El usuario ya existe'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not data or 'usuario' not in data or 'contraseña' not in data:
        return jsonify({'error': 'Datos incompletos'}), 400
    
    usuario = data['usuario']
    contraseña = data['contraseña']
    
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id, password FROM usuarios WHERE usuario = ?', (usuario,))
            user = cursor.fetchone()
        
        if user and check_password_hash(user[1], contraseña):
            return jsonify({'mensaje': 'Inicio de sesión exitoso', 'usuario_id': user[0]}), 200
        else:
            return jsonify({'error': 'Credenciales inválidas'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/tareas', methods=['GET'])
def tareas():
    return render_template('bienvenida.html')

if __name__ == '__main__':
  
    if not os.path.exists('templates'):
        os.makedirs('templates')
    app.run(debug=True)