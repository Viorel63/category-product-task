class Product:
    def __init__(self, name: str, description: str, price: float, quantity: int):
        self.name = name
        self.description = description
        self._price = price  # Защищенный атрибут
        self.quantity = quantity

    @classmethod
    def create_product(cls, name: str, description: str, price: float, quantity: int, products: list = None):
        """Создает товар с проверкой дубликатов"""
        if products:
            for product in products:
                if product.name == name:
                    product.quantity += quantity
                    if price > product.price:
                        product.price = price
                    return product
        return cls(name, description, price, quantity)

    @property
    def price(self):
        """Геттер для цены"""
        return self._price

    @price.setter
    def price(self, value):
        """Сеттер для цены с проверкой"""
        if value <= 0:
            print("Цена введена некорректная")
        else:
            self._price = value


class Category:
    total_categories = 0
    total_unique_products = 0

    def __init__(self, name: str, description: str, products: list = None):
        self.name = name
        self.description = description
        self.__products = products if products else []
        Category.total_categories += 1
        Category.total_unique_products += len(set(self.__products))

    def add_product(self, product):
        """Добавляет товар в категорию"""
        if isinstance(product, Product):
            self.__products.append(product)
            Category.total_unique_products = len(set(self.__products))
        else:
            raise TypeError("Можно добавлять только объекты класса Product")

    @property
    def products(self):
        """Возвращает форматированный список товаров"""
        return "\n".join(
            f"{product.name}: {product.price} руб. Остаток: {product.quantity} шт."
            for product in self.__products
        )