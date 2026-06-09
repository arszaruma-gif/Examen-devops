import os
from dotenv import load_dotenv
from flask import Flask, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor

load_dotenv()

app = Flask(__name__)

APP_NAME = os.environ.get('APP_NAME', 'Sistema Inventario')
APP_VERSION = os.environ.get('APP_VERSION', '1.0.0')

def get_db_connection():
    return psycopg2.connect(
        host=os.environ.get('DB_HOST', 'db'),
        database=os.environ.get('DB_NAME', 'empresa'),
        user=os.environ.get('DB_USER', 'admin'),
        password=os.environ.get('DB_PASSWORD', 'admin123'),
        port=os.environ.get('DB_PORT', '5432')
    )

@app.route('/')
def home():
    try:
        conn = get_db_connection()
        conn.close()

        return jsonify({
            "aplicacion": APP_NAME,
            "version": APP_VERSION,
            "postgresql": "Conectado"
        }), 200

    except Exception as e:
        return jsonify({
            "aplicacion": APP_NAME,
            "version": APP_VERSION,
            "postgresql": f"Error: {str(e)}"
        }), 500


@app.route('/productos')
def listar_productos():

    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)

        cur.execute("""
            SELECT id, nombre, precio, stock
            FROM productos
        """)

        productos = cur.fetchall()

        cur.close()
        conn.close()

        return jsonify(productos), 200

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)