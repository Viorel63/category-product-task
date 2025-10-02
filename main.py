from src.models import Product, Smartphone, LawnGrass, Category, Order


def main():
    print("=== Создание продуктов ===")
    product = Product("Книга", "Интересная книга", 500.0, 10)
    phone = Smartphone("iPhone", "Флагман", 100000.0, 5,
                       "A15 Bionic", "15 Pro", 256, "Black")
    grass = LawnGrass("Элитная трава", "Для гольфа", 3000.0, 20,
                      "США", 21, "Изумрудный")

    print("\n=== Создание категории ===")
    category = Category("Электроника", "Технические товары", [product, phone])

    print("\n=== Создание заказа ===")
    order = Order("Мой заказ", "Заказ телефона", phone, 2)

    print("\n=== Проверка repr ===")
    print(repr(product))
    print(repr(phone))
    print(repr(grass))
    print(repr(category))
    print(repr(order))

    print("\n=== Информация о заказе ===")
    print(order)


if __name__ == "__main__":
    main()