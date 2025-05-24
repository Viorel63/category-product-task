import pytest
from models import Product, Category

@pytest.fixture
def sample_product():
    return Product("Телефон", "Смартфон", 50000.0, 10)

def test_product_init(sample_product):
    assert sample_product.name == "Телефон"
    assert sample_product.price == 50000.0
