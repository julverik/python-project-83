import psycopg2
from psycopg2.extras import RealDictCursor
from .config import Config

def get_connection():
    """Подключение к базе данных"""
    return psycopg2.connect(Config.DATABASE_URL)

def get_urls():
    """Получить все URL, сортировка по убыванию ID (новые первыми)"""
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute('SELECT * FROM urls ORDER BY id DESC')
            return cur.fetchall()

def get_url(url_id):
    """Получить URL по ID"""
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute('SELECT * FROM urls WHERE id = %s', (url_id,))
            return cur.fetchone()

def add_url(name):
    """Добавить URL в базу, если его нет"""
    if name.endswith('/'):
        name = name[:-1]
    
    with get_connection() as conn:
        with conn.cursor() as cur:
            try:
                cur.execute(
                    'INSERT INTO urls (name) VALUES (%s) RETURNING id',
                    (name,)
                )
                conn.commit()
                return cur.fetchone()[0]
            except psycopg2.IntegrityError:
                conn.rollback()
                cur.execute('SELECT id FROM urls WHERE name = %s', (name,))
                return cur.fetchone()[0]