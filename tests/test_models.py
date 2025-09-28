import pytest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.models import Product, Smartphone, LawnGrass, Category


@pytest.fixture
def sample_product():
    return Product("Телефон", "Смартфон", 50000.0, 10)


@pytest.fixture
def sample_smartphone():
    return Smartphone("iPhone", "Флагманский смартфон", 100000.0, 5,
                      "A15 Bionic", "15 Pro", 256, "Black")


@pytest.fixture
def sample_lawn_grass():
    return LawnGrass("Газонная трава", "Для спортивных площадок", 1500.0, 20,
                     "Германия", 14, "Зеленый")


@pytest.fixture
def sample_category():
    product1 = Product("Клавиатура", "Механическая", 5000.0, 10)
    product2 = Smartphone("Samsung", "Android смартфон", 80000.0, 3,
                          "Snapdragon 8", "Galaxy S23", 128, "White")
    return Category("Электроника", "Техника", [product1, product2])


def test_smartphone_creation():
    """Тест создания смартфона"""
    phone = Smartphone("Xiaomi", "Бюджетный смартфон", 25000.0, 8,
                       "Snapdragon 7", "Redmi Note 12", 64, "Blue")

    assert phone.name == "Xiaomi"
    assert phone.price == 25000.0
    assert phone.performance == "Snapdragon 7"
    assert phone.model == "Redmi Note 12"
    assert phone.storage == 64
    assert phone.color == "Blue"


def test_lawn_grass_creation():
    """Тест создания газонной травы"""
    grass = LawnGrass("Универсальная трава", "Для дачных участков", 1200.0, 15,
                      "Россия", 10, "Темно-зеленый")

    assert grass.name == "Универсальная трава"
    assert grass.price == 1200.0
    assert grass.country == "Россия"
    assert grass.germination_period == 10
    assert grass.color == "Темно-зеленый"


def test_product_addition_same_type():
    """Тест сложения товаров одного типа"""
    product1 = Product("Товар1", "Описание1", 100.0, 2)
    product2 = Product("Товар2", "Описание2", 200.0, 3)
    total = product1 + product2
    assert total == 100 * 2 + 200 * 3  # 200 + 600 = 800


def test_smartphone_addition_same_type(sample_smartphone):
    """Тест сложения смартфонов одного типа"""
    phone2 = Smartphone("iPhone", "Старая модель", 50000.0, 2,
                        "A14 Bionic", "14 Pro", 128, "White")
    total = sample_smartphone + phone2
    assert total == 100000 * 5 + 50000 * 2  # 500000 + 100000 = 600000


def test_product_addition_different_types(sample_product, sample_smartphone):
    """Тест ошибки при сложении товаров разных типов"""
    with pytest.raises(TypeError, match="Можно складывать только товары одного класса"):
        sample_product + sample_smartphone


def test_smartphone_addition_with_product(sample_smartphone, sample_product):
    """Тест ошибки при сложении смартфона с обычным товаром"""
    with pytest.raises(TypeError, match="Можно складывать только товары одного класса"):
        sample_smartphone + sample_product


def test_add_product_type_check():
    """Тест проверки типа при добавлении товара в категорию"""
    category = Category("Тест", "Тестовая категория")

    # Можно добавить Product
    product = Product("Товар", "Описание", 100.0, 1)
    category.add_product(product)

    # Можно добавить Smartphone (наследник Product)
    phone = Smartphone("Телефон", "Смартфон", 50000.0, 1, "Процессор", "Модель", 128, "Черный")
    category.add_product(phone)

    # Можно добавить LawnGrass (наследник Product)
    grass = LawnGrass("Трава", "Газонная", 1000.0, 1, "Россия", 10, "Зеленый")
    category.add_product(grass)

    # Нельзя добавить не-Product
    with pytest.raises(TypeError, match="Можно добавлять только объекты класса Product или его наследников"):
        category.add_product("не товар")


def test_category_mixed_products():
    """Тест категории со смешанными типами товаров"""
    category = Category("Разные товары", "Категория с разными типами товаров")

    # Добавляем товары разных типов
    product = Product("Мышь", "Компьютерная мышь", 1500.0, 5)
    phone = Smartphone("Google Pixel", "Android смартфон", 60000.0, 2,
                       "Tensor G2", "7 Pro", 256, "Gray")
    grass = LawnGrass("Элитная трава", "Для гольф-полей", 3000.0, 10,
                      "США", 21, "Изумрудный")

    category.add_product(product)
    category.add_product(phone)
    category.add_product(grass)

    # Проверяем что все добавились
    assert len(category._Category__products) == 3
    assert len(category) == 17  # 5 + 2 + 10


def test_inheritance():
    """Тест наследования"""
    phone = Smartphone("Тест", "Тест", 100.0, 1, "Перф", "Модель", 64, "Цвет")
    grass = LawnGrass("Тест", "Тест", 100.0, 1, "Страна", 10, "Цвет")

    # Проверяем что наследники являются Product
    assert isinstance(phone, Product)
    assert isinstance(grass, Product)

    # Проверяем что наследники имеют все методы родителя
    assert hasattr(phone, 'price')
    assert hasattr(phone, 'quantity')
    assert hasattr(grass, 'price')
    assert hasattr(grass, 'quantity')

# Остальные существующие тесты остаются без изменений...