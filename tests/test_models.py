import pytest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.models import (Product, Smartphone, LawnGrass, Category, Order,
                        AbstractProduct, AbstractCategory, ReprMixin)


def test_abstract_product_instantiation():
    """Тест что нельзя создать экземпляр абстрактного класса"""
    with pytest.raises(TypeError):
        AbstractProduct("Тест", "Тест", 100.0, 1)


def test_abstract_category_instantiation():
    """Тест что нельзя создать экземпляр абстрактного класса категории"""
    with pytest.raises(TypeError):
        AbstractCategory("Тест", "Тест")


def test_repr_mixin_product():
    """Тест миксина ReprMixin для Product"""
    product = Product("Тестовый товар", "Описание", 100.0, 5)
    repr_str = repr(product)
    assert "Product(" in repr_str
    assert "'Тестовый товар'" in repr_str


def test_repr_mixin_smartphone():
    """Тест миксина ReprMixin для Smartphone"""
    phone = Smartphone("Телефон", "Смартфон", 50000.0, 2,
                       "Процессор", "Модель", 128, "Черный")
    repr_str = repr(phone)
    assert "Smartphone(" in repr_str
    assert "'Телефон'" in repr_str
    assert "128" in repr_str


def test_order_creation():
    """Тест создания заказа"""
    product = Product("Книга", "Интересная книга", 500.0, 10)
    order = Order("Мой заказ", "Заказ книги", product, 3)

    assert order.name == "Мой заказ"
    assert order.product == product
    assert order.quantity == 3
    assert order.total_price == 1500.0  # 500 * 3


def test_order_str():
    """Тест строкового представления заказа"""
    product = Product("Книга", "Интересная книга", 500.0, 10)
    order = Order("Мой заказ", "Заказ книги", product, 3)

    order_str = str(order)
    assert "Заказ: Мой заказ" in order_str
    assert "Товар: Книга" in order_str
    assert "Количество: 3 шт." in order_str
    assert "Итоговая стоимость: 1500 руб." in order_str


def test_order_length():
    """Тест длины заказа"""
    product = Product("Книга", "Интересная книга", 500.0, 10)
    order = Order("Мой заказ", "Заказ книги", product, 3)

    assert len(order) == 3


def test_common_abstract_class():
    """Тест общего абстрактного класса для Category и Order"""
    product = Product("Товар", "Описание", 100.0, 5)
    category = Category("Категория", "Описание категории")
    order = Order("Заказ", "Описание заказа", product, 2)

    # Оба класса должны наследовать от AbstractCategory
    assert isinstance(category, AbstractCategory)
    assert isinstance(order, AbstractCategory)

    # Оба должны иметь обязательные методы
    assert hasattr(category, '__str__')
    assert hasattr(category, '__len__')
    assert hasattr(order, '__str__')
    assert hasattr(order, '__len__')

# Остальные существующие тесты остаются...