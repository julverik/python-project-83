import requests
from flask import (
    Flask,
    flash,
    get_flashed_messages,
    redirect,
    render_template,
    request,
    url_for,
)

from . import db, parser, validate
from .config import Config

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

    checks = db.get_checks(url_id)
    messages = get_flashed_messages(with_categories=True)
    return render_template(
        'url.html',
        url=url,
        checks=checks,
        messages=messages
    )


@app.route('/urls', methods=['POST'])
def add_url():
    """Добавление нового URL"""
    raw_url = request.form.get('url', '').strip()

    is_valid, error_message = validate.validate_url(raw_url)

    if not is_valid:
        flash(error_message, 'error')
        messages = get_flashed_messages(with_categories=True)
        return render_template('index.html', messages=messages), 422

    normalized_url = validate.normalize_url(raw_url)

    existing_url = db.get_url_by_name(normalized_url)
    if existing_url:
        flash('Страница уже существует', 'info')
        return redirect(url_for('url_detail', url_id=existing_url['id']))

    try:
        url_id = db.add_url(normalized_url)
        flash('Страница успешно добавлена', 'success')
        return redirect(url_for('url_detail', url_id=url_id))
    except Exception:
        flash('Ошибка при добавлении URL', 'error')
        return redirect(url_for('index'))


@app.route('/urls/<int:url_id>/checks', methods=['POST'])
def check_url(url_id):
    """Запустить проверку URL"""
    url = db.get_url(url_id)
    if not url:
        flash('Страница не найдена', 'error')
        return redirect(url_for('urls_list'))

    try:
        response = requests.get(url['name'], timeout=5)
        response.raise_for_status()

        seo_data = parser.parse_html(response.text)

        db.add_check(
            url_id,
            status_code=response.status_code,
            h1=seo_data['h1'],
            title=seo_data['title'],
            description=seo_data['description']
        )

        flash('Страница успешно проверена', 'success')

    except requests.RequestException:
        flash('Произошла ошибка при проверке', 'error')
    except Exception:
        flash('Произошла ошибка при проверке', 'error')

    return redirect(url_for('url_detail', url_id=url_id))