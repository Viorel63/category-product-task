import pytest
from models import Product, Category

@pytest.fixture
def sample_product():
    return Product("Телефон", "Смартфон", 50000.0, 10)

@pytest.fixture
def sample_category():
    return Category("Электроника", "Техника")

def test_price_setter(capsys):
    """Проверка сеттера цены"""
    prod = Product("Тест", "Тест", 100.0, 1)
    prod.price = -50
    captured = capsys.readouterr()
    assert "Цена введена некорректная" in captured.out
    assert prod.price == 100.0  # Цена не должна измениться

def test_product_creation():
    """Проверка создания товара с дубликатами"""
    existing = [Product("Клавиатура", "Механическая", 5000.0, 10)]
    new = Product.create_product(
        "Клавиатура",
        "Механическая",
        5500.0,
        5,
        existing
    )
    assert new.quantity == 15  # 10 + 5
    assert new.price == 5500.0  # Выбрана большая цена

def test_add_product(sample_category, sample_product):
    """Проверка добавления товара в категорию"""
    sample_category.add_product(sample_product)
    assert "Телефон" in sample_category.products
    assert sample_product in sample_category._Category__products  # Проверка приватного атрибута