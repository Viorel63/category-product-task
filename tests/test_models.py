import pytest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.models import Product, Category, CategoryIterator


@pytest.fixture
def sample_product():
    return Product("Телефон", "Смартфон", 50000.0, 10)


@pytest.fixture
def sample_category():
    product1 = Product("Телефон", "Смартфон", 50000.0, 10)
    product2 = Product("Ноутбук", "Игровой", 100000.0, 5)
    return Category("Электроника", "Техника", [product1, product2])


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


def test_add_product(sample_category):
    """Проверка добавления товара в категорию"""
    # Создаем товар с УНИКАЛЬНЫМ именем, которого нет в категории
    new_product = Product("Планшет", "Графический планшет", 30000.0, 3)

    initial_count = len(sample_category._Category__products)
    sample_category.add_product(new_product)

    # Проверяем что товар добавился в список
    assert len(sample_category._Category__products) == initial_count + 1

    # Проверяем что товар есть в строковом представлении
    assert "Планшет" in sample_category.products

    # Проверяем что последний добавленный товар имеет правильное имя
    assert sample_category._Category__products[-1].name == "Планшет"


def test_add_duplicate_product(sample_category):
    """Тест добавления дубликата товара"""
    # Добавляем товар с существующим именем "Телефон"
    initial_product_count = len(sample_category._Category__products)
    initial_total_quantity = len(sample_category)

    duplicate_product = Product("Телефон", "Новая модель", 60000.0, 3)
    sample_category.add_product(duplicate_product)

    # Количество товаров в списке не должно измениться (дубликат не добавляется)
    assert len(sample_category._Category__products) == initial_product_count

    # Общее количество товаров должно увеличиться
    assert len(sample_category) == initial_total_quantity + 3  # 15 + 3 = 18

    # Цена должна обновиться до максимальной
    for product in sample_category._Category__products:
        if product.name == "Телефон":
            assert product.price == 60000.0
            assert product.quantity == 13  # 10 + 3
            break


def test_product_str(sample_product):
    """Тест строкового представления Product"""
    expected = "Телефон, 50000.0 руб. Остаток: 10 шт."
    assert str(sample_product) == expected


def test_category_str(sample_category):
    """Тест строкового представления Category"""
    expected = "Электроника, количество продуктов: 15 шт."
    assert str(sample_category) == expected


def test_category_len(sample_category):
    """Тест метода __len__ для Category"""
    assert len(sample_category) == 15  # 10 + 5


def test_product_len(sample_product):
    """Тест метода __len__ для Product"""
    assert len(sample_product) == 10


def test_product_addition(sample_product):
    """Тест сложения продуктов"""
    product2 = Product("Планшет", "Графический", 30000.0, 3)
    total = sample_product + product2
    expected = 50000.0 * 10 + 30000.0 * 3  # 500000 + 90000 = 590000
    assert total == expected


def test_product_addition_type_error(sample_product):
    """Тест ошибки типа при сложении"""
    with pytest.raises(TypeError, match="Можно складывать только объекты класса Product"):
        sample_product + "invalid"


def test_category_iteration(sample_category):
    """Тест итерации по категории"""
    products = list(sample_category)
    assert len(products) == 2
    assert all(isinstance(p, Product) for p in products)


def test_category_iterator(sample_category):
    """Тест класса CategoryIterator"""
    iterator = CategoryIterator(sample_category)
    products = list(iterator)
    assert len(products) == 2
    assert products[0].name == "Телефон"
    assert products[1].name == "Ноутбук"


def test_add_duplicate_product(sample_category):
    """Тест добавления дубликата товара"""
    initial_len = len(sample_category)
    duplicate_product = Product("Телефон", "Новая модель", 60000.0, 3)
    sample_category.add_product(duplicate_product)

    # Количество должно увеличиться, но не добавится новый продукт
    assert len(sample_category) == initial_len + 3  # 15 + 3 = 18

    # Цена должна обновиться до максимальной
    for product in sample_category._Category__products:
        if product.name == "Телефон":
            assert product.price == 60000.0
            break