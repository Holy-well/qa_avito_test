import requests
import pytest

BASE_URL = "https://qa-internship.avito.com/api/1"
SELLER_ID = 323252  # Из документации

@pytest.fixture
def create_listing():
    """Фикстура для создания объявления"""
    payload = {
        "name": "Телефон",
        "price": 85566,
        "sellerId": SELLER_ID,
        "statistics": {
            "contacts": 32,
            "like": 35,
            "viewCount": 14
        }
    }
    response = requests.post(f"{BASE_URL}/item", json=payload, timeout=5)
    assert response.status_code == 200
    # Извлечение ID из строки
    listing_id = response.json()["status"].split(' - ')[1]  # Получаем ID из строки
    return listing_id


def test_create_listing():
    """Тест на создание объявления"""
    url = f"{BASE_URL}/item"
    payload = {
        "name": "Телефон",
        "price": 85566,
        "sellerId": SELLER_ID,
        "statistics": {
            "contacts": 32,
            "like": 35,
            "viewCount": 14
        }
    }
    response = requests.post(url, json=payload, timeout=5)
    assert response.status_code == 200  # Корректируем ожидание статуса на 200
    json_response = response.json()
    assert "id" in json_response  # Убеждаемся, что "id" есть в ответе
    assert json_response["name"] == "Телефон"
    assert json_response["price"] == 85566

def test_get_listing_by_id(create_listing):
    """Тест на получение объявления по ID"""
    listing_id = create_listing
    get_url = f"{BASE_URL}/item/{listing_id}"
    get_response = requests.get(get_url, timeout=5)
    assert get_response.status_code == 200
    json_response = get_response.json()
    assert json_response["name"] == "Телефон"
    assert json_response["price"] == 85566

def test_get_all_listings_by_seller():
    """Тест на получение всех объявлений по продавцу"""
    for i in range(3):
        payload = {
            "name": f"Товар {i}",
            "price": 10000 + i * 1000,
            "sellerId": SELLER_ID,
            "statistics": {
                "contacts": 10 + i,
                "like": 5 + i,
                "viewCount": 20 + i
            }
        }
        response = requests.post(f"{BASE_URL}/item", json=payload, timeout=5)
        assert response.status_code == 200  # Убедитесь, что сервер возвращает 200

    # Получаем все объявления продавца
    get_url = f"{BASE_URL}/{SELLER_ID}/item"
    get_response = requests.get(get_url, timeout=5)
    assert get_response.status_code == 200
    listings = get_response.json()
    assert len(listings) >= 3  # Проверка на количество объявлений

def test_create_listing_invalid_data():
    """Тест на создание объявления с некорректными данными"""
    url = f"{BASE_URL}/item"
    payload = {
        "name": "Телефон",
        # Отсутствует обязательное поле price
        "sellerId": SELLER_ID,
        "statistics": {
            "contacts": 32,
            "like": 35,
            "viewCount": 14
        }
    }
    response = requests.post(url, json=payload, timeout=5)
    assert response.status_code == 400  # Если API должен возвращать 400 при некорректных данных

def test_get_listing_invalid_id():
    """Тест на получение объявления с несуществующим ID"""
    invalid_id = "123e4567-e89b-12d3-a456-426614174000"
    get_url = f"{BASE_URL}/item/{invalid_id}"
    response = requests.get(get_url, timeout=5)
    assert response.status_code == 404
    assert "message" in response.json()["result"]  # Проверка сообщения об ошибке
