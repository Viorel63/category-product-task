import pytest
from models import Product, Category, CategoryIterator


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


def test_add_product(sample_category, sample_product):
    """Проверка добавления товара в категорию"""
    sample_category.add_product(sample_product)
    assert "Телефон" in sample_category.products
    assert sample_product in sample_category._Category__products


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