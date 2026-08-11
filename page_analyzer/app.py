from flask import Flask, render_template, request, redirect, url_for, flash, get_flashed_messages
from .config import Config
from . import db
from . import validate

app = Flask(__name__)
app.config.from_object(Config)


@app.route('/')
def index():
    """Главная страница"""
    messages = get_flashed_messages(with_categories=True)
    return render_template('index.html', messages=messages)


@app.route('/urls', methods=['GET'])
def urls_list():
    """Список всех добавленных URL"""
    urls = db.get_urls()
    messages = get_flashed_messages(with_categories=True)
    return render_template('urls.html', urls=urls, messages=messages)


@app.route('/urls/<int:url_id>')
def url_detail(url_id):
    """Детальная страница URL"""
    url = db.get_url(url_id)
    if not url:
        flash('Страница не найдена', 'error')
        return redirect(url_for('urls_list'))
    messages = get_flashed_messages(with_categories=True)
    return render_template('url.html', url=url, messages=messages)


@app.route('/urls', methods=['POST'])
def add_url():
    """Добавление нового URL"""
    raw_url = request.form.get('url', '').strip()
    
    is_valid, error_message = validate.validate_url(raw_url)
    
    if not is_valid:
        flash(error_message, 'error')
        return redirect(url_for('index'))
    
    normalized_url = validate.normalize_url(raw_url)
    
    try:
        url_id = db.add_url(normalized_url)
        flash('Страница успешно добавлена', 'success')
        return redirect(url_for('url_detail', url_id=url_id))
    except Exception:
        flash('Ошибка при добавлении URL', 'error')
        return redirect(url_for('index'))
