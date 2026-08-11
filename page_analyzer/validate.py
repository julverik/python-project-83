from urllib.parse import urlparse

import validators


def validate_url(url):
    """Проверяет URL на корректность."""
    if not url or not url.strip():
        return False, 'URL не может быть пустым'
    
    url = url.strip()
    
    if len(url) > 255:
        return False, 'URL превышает 255 символов'
    
    if not url.startswith('http://') and not url.startswith('https://'):
        return False, 'Некорректный URL. Введите адрес, начиная с http:// или https://'
    
    if not validators.url(url):
        return False, 'Некорректный формат URL'
    
    return True, None


def normalize_url(url):
    """Нормализует URL"""
    if not url:
        return url

    url = url.strip()

    parsed = urlparse(url)
    normalized = f"{parsed.scheme}://{parsed.netloc.lower()}"

    return normalized