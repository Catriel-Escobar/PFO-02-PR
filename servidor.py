from flask import Flask, request, jsonify, render_template
import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)


DB_PATH = 'tareas.db'


def init_db():
    conn = sqlite3.connect(DB_PATH)
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
    conn.close()

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
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO usuarios (usuario, password) VALUES (?, ?)', 
                      (usuario, hashed_password))
        conn.commit()
        conn.close()
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
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('SELECT id, password FROM usuarios WHERE usuario = ?', (usuario,))
        user = cursor.fetchone()
        conn.close()
        
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