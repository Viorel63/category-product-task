class Product:
    def __init__(self, name: str, description: str, price: float, quantity: int):
        self.name = name
        self.description = description
        self._price = price  # Защищенный атрибут
        self.quantity = quantity

    def __str__(self) -> str:
        """Строковое представление для задания 1"""
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other) -> float:
        """Сложение продуктов для задания 2"""
        if not isinstance(other, Product):
            raise TypeError("Можно складывать только объекты класса Product")
        return self.price * self.quantity + other.price * other.quantity

    def __len__(self) -> int:
        """Возвращает количество товара на складе"""
        return self.quantity

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
        Category.total_unique_products = len(set(self.__products))

    def __str__(self) -> str:
        """Строковое представление для задания 1"""
        total_quantity = sum(product.quantity for product in self.__products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."

    def __len__(self) -> int:
        """Возвращает общее количество товаров в категории"""
        return sum(product.quantity for product in self.__products)

    def __iter__(self):
        """Итератор для дополнительного задания"""
        self._current_index = 0
        return self

    def __next__(self):
        """Возвращает следующий товар в категории"""
        if self._current_index < len(self.__products):
            product = self.__products[self._current_index]
            self._current_index += 1
            return product
        raise StopIteration

    def add_product(self, product):
        """Добавляет товар в категорию"""
        if isinstance(product, Product):
            # Проверяем, есть ли уже такой товар
            for existing_product in self.__products:
                if existing_product.name == product.name:
                    existing_product.quantity += product.quantity
                    if product.price > existing_product.price:
                        existing_product.price = product.price
                    return

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


class CategoryIterator:
    """Итератор для категории (дополнительное задание)"""

    def __init__(self, category):
        self._category = category
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._index < len(self._category._Category__products):
            product = self._category._Category__products[self._index]
            self._index += 1
            return product
        raise StopIteration