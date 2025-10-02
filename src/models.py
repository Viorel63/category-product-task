from abc import ABC, abstractmethod


class ReprMixin:
    """Миксин для вывода информации о создании объекта"""

    def __repr__(self):
        attrs = []
        for attr, value in self.__dict__.items():
            # Форматируем строковые значения
            if isinstance(value, str):
                attrs.append(f"'{value}'")
            else:
                attrs.append(str(value))

        class_name = self.__class__.__name__
        return f"{class_name}({', '.join(attrs)})"


class AbstractProduct(ABC):
    """Абстрактный класс для продуктов"""

    @abstractmethod
    def __init__(self, name: str, description: str, price: float, quantity: int):
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def __add__(self, other):
        pass


class Product(AbstractProduct, ReprMixin):
    def __init__(self, name: str, description: str, price: float, quantity: int):
        print(f"Создан объект: {self.__class__.__name__}('{name}', '{description}', {price}, {quantity})")
        self.name = name
        self.description = description
        self._price = price
        self.quantity = quantity

    def __str__(self) -> str:
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other) -> float:
        if type(other) is not type(self):
            raise TypeError("Можно складывать только товары одного класса")
        return self.price * self.quantity + other.price * other.quantity

    def __len__(self) -> int:
        return self.quantity

    @classmethod
    def create_product(cls, name: str, description: str, price: float, quantity: int, products: list = None):
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
        return self._price

    @price.setter
    def price(self, value):
        if value <= 0:
            print("Цена введена некорректная")
        else:
            self._price = value


class Smartphone(Product, ReprMixin):
    def __init__(self, name: str, description: str, price: float, quantity: int,
                 performance: str, model: str, storage: int, color: str):
        print(f"Создан объект: {self.__class__.__name__}('{name}', '{description}', {price}, {quantity}, "
              f"'{performance}', '{model}', {storage}, '{color}')")

        super().__init__(name, description, price, quantity)
        self.performance = performance
        self.model = model
        self.storage = storage
        self.color = color

    def __str__(self) -> str:
        return (f"{self.name} ({self.model}), {self.price} руб. Остаток: {self.quantity} шт.\n"
                f"Характеристики: {self.performance}, {self.storage}GB, {self.color}")


class LawnGrass(Product, ReprMixin):
    def __init__(self, name: str, description: str, price: float, quantity: int,
                 country: str, germination_period: int, color: str):
        print(f"Создан объект: {self.__class__.__name__}('{name}', '{description}', {price}, {quantity}, "
              f"'{country}', {germination_period}, '{color}')")

        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color

    def __str__(self) -> str:
        return (f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт.\n"
                f"Производитель: {self.country}, прорастание: {self.germination_period} дней, цвет: {self.color}")


class AbstractCategory(ABC):
    """Абстрактный класс для категорий и заказов"""

    @abstractmethod
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def __len__(self):
        pass


class Category(AbstractCategory, ReprMixin):
    total_categories = 0
    total_unique_products = 0

    def __init__(self, name: str, description: str, products: list = None):
        print(f"Создан объект: {self.__class__.__name__}('{name}', '{description}', {products})")

        super().__init__(name, description)
        self.__products = products if products else []
        Category.total_categories += 1
        Category.total_unique_products = len(set(self.__products))

    def __str__(self) -> str:
        total_quantity = sum(product.quantity for product in self.__products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."

    def __len__(self) -> int:
        return sum(product.quantity for product in self.__products)

    def __iter__(self):
        self._current_index = 0
        return self

    def __next__(self):
        if self._current_index < len(self.__products):
            product = self.__products[self._current_index]
            self._current_index += 1
            return product
        raise StopIteration

    def add_product(self, product):
        """Добавляет товар в категорию с проверкой типа"""
        if not isinstance(product, Product):
            raise TypeError("Можно добавлять только объекты класса Product или его наследников")

        # Проверяем, есть ли уже такой товар
        for existing_product in self.__products:
            if existing_product.name == product.name:
                existing_product.quantity += product.quantity
                if product.price > existing_product.price:
                    existing_product.price = product.price
                return

        self.__products.append(product)
        Category.total_unique_products = len(set(self.__products))

    @property
    def products(self):
        return "\n".join(
            f"{product.name}: {product.price} руб. Остаток: {product.quantity} шт."
            for product in self.__products
        )


class Order(AbstractCategory, ReprMixin):
    """Класс для заказа (дополнительное задание)"""

    def __init__(self, name: str, description: str, product: Product, quantity: int):
        print(f"Создан объект: {self.__class__.__name__}('{name}', '{description}', {product}, {quantity})")

        super().__init__(name, description)
        self.product = product
        self.quantity = quantity
        self.total_price = product.price * quantity

    def __str__(self) -> str:
        return (f"Заказ: {self.name}\n"
                f"Товар: {self.product.name}\n"
                f"Количество: {self.quantity} шт.\n"
                f"Итоговая стоимость: {self.total_price} руб.")

    def __len__(self) -> int:
        return self.quantity


class CategoryIterator(ReprMixin):
    def __init__(self, category):
        print(f"Создан объект: {self.__class__.__name__}({category})")
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