import psycopg2
from psycopg2.extras import RealDictCursor
from .config import Config

def get_connection():
    """Подключение к базе данных"""
    return psycopg2.connect(Config.DATABASE_URL)

def get_urls():
    """Получить все URL с датой последней проверки и кодом ответа"""
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT 
                    urls.*,
                    (SELECT created_at FROM url_checks 
                     WHERE url_id = urls.id 
                     ORDER BY id DESC LIMIT 1) as last_check_at,
                    (SELECT status_code FROM url_checks 
                     WHERE url_id = urls.id 
                     ORDER BY id DESC LIMIT 1) as last_status_code
                FROM urls 
                ORDER BY urls.id DESC
            """)
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

def get_checks(url_id):
    """Получить все проверки для URL"""
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                'SELECT * FROM url_checks WHERE url_id = %s ORDER BY id DESC',
                (url_id,)
            )
            return cur.fetchall()

def add_check(url_id, status_code):
    """Добавить новую проверку с кодом ответа"""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                'INSERT INTO url_checks (url_id, status_code) VALUES (%s, %s) RETURNING id',
                (url_id, status_code)
            )
            conn.commit()
            return cur.fetchone()[0]