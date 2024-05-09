import pytest
from shop import Shop

@pytest.fixture
def shop():
    return Shop()

def test_unknown_command(shop):
    result = shop.process("Неизвестная комманда")
    assert(result.lower() == 
    "невозможно выполнить комманду 'неизвестная комманда'\n")

def test_add_catalog(shop):
    result = shop.process(
            "Добавить книгу Название1 Автор1 2000 1250 Издательство1 Жанр1")
    assert(result.lower() == 
    "книга название1 автор1 2000 1250 издательство1 жанр1 успешно добавлена\n")
    
def test_view_catalog(shop):
    shop.process("Добавить книгу Название1 Автор1 2000 1250 Издательство1 Жанр1")
    shop.process("Добавить книгу Название2 Автор2 1900 2500 Издательство2 Жанр2")
    catalog = shop.process("Просмотреть каталог")
    assert (catalog.lower() == "название1 автор1 2000 1250 издательство1 жанр1\nназвание2 автор2 1900 2500 издательство2 жанр2\n")  

def test_cart_adding_deleting(shop):
    shop.process("Добавить книгу Название1 Автор1 2000 1250 Издательство1 Жанр1")
    shop.process("Добавить книгу Название2 Автор2 1900 2500 Издательство2 Жанр2")

    res = shop.process("Положить в корзину книгу Название1")
    assert (res.lower() == "книга название1 успешно добавлена в корзину")
    res = shop.process("Положить в корзину книгу Название2")
    assert (res.lower() == "книга название2 успешно добавлена в корзину")

    cart = shop.process("Просмотреть содержимое корзины")
    assert (cart.lower() == "название1 автор1 2000 1250 издательство1 жанр1\nназвание2 автор2 1900 2500 издательство2 жанр2\n")

    shop.process("Удалить из корзины Название2")
    cart = shop.process("Просмотреть содержимое корзины")
    assert (cart.lower() == "название1 автор1 2000 1250 издательство1 жанр1\n")

def test_add_unknown_in_cart(shop):
    shop.process("Добавить книгу Название1 Автор1 2000 1250 Издательство1 Жанр1")
    res = shop.process("Положить в корзину книгу Название1")

    res = shop.process("Положить в корзину книгу Название2")
    assert (res.lower() == "книги название2 нет в каталоге")

    cart = shop.process("Просмотреть содержимое корзины")
    assert (cart.lower() == "название1 автор1 2000 1250 издательство1 жанр1\n")

def test_delete_unknown_from_cart(shop):
    shop.process("Добавить книгу Название1 Автор1 2000 1250 Издательство1 Жанр1")
    res = shop.process("Положить в корзину книгу Название1")

    res = shop.process("Удалить из корзины Название2")
    assert (res.lower() == "книги название2 нет в корзине")

    cart = shop.process("Просмотреть содержимое корзины")
    assert (cart.lower() == "название1 автор1 2000 1250 издательство1 жанр1\n")

def test_delivery_decline(shop):
    shop.process("Добавить книгу Название1 Автор1 2000 1250 Издательство1 Жанр1")
    shop.process("Добавить книгу Название2 Автор2 1900 2500 Издательство2 Жанр2")

    shop.process("Положить в корзину книгу Название1")
    order_status = shop.process("Оформить заказ Адрес Время Оплата_при_получении")
    assert (order_status.lower() == "заказ 0 оформлен адрес время оплата_при_получении\n")

    declined_order = shop.process("Отменить заказ 0 с_курьером Адрес Время")
    assert (declined_order.lower() == "заказ 0 отменен с_курьером адрес время: название1 автор1 2000 1250 издательство1 жанр1\n")

def test_delivery_empty(shop):
    order_status = shop.process("Оформить заказ Адрес Время Оплата_при_получении")
    assert (order_status.lower() == "корзина пуста\n")

def test_decline_empty(shop):
    declined_order = shop.process("Отменить заказ 0 с_курьером Адрес Время")
    assert (declined_order.lower() == "не существует заказа\n")

def test_delivered(shop):
    shop.process("Добавить книгу Название1 Автор1 2000 1250 Издательство1 Жанр1")
    shop.process("Положить в корзину книгу Название1")
    shop.process("Оформить заказ Адрес Время Оплата_при_получении")

    result = shop.process("Доставить заказ 0")
    assert (result.lower() == "доставлен заказ 0 название1 автор1 2000 1250 издательство1 жанр1\n")

def test_delivered_unknown(shop):
    result = shop.process("Доставить заказ 0")
    assert (result.lower() == "не существует заказа 0")

def test_refunded(shop):
    shop.process("Добавить книгу Название1 Автор1 2000 1250 Издательство1 Жанр1")
    shop.process("Положить в корзину книгу Название1")
    shop.process("Оформить заказ Адрес Время Оплата_при_получении")
    declined_order = shop.process("Отменить заказ 0 с_курьером Адрес Время")

    result = shop.process("Принять возврат заказа 0")
    assert (result.lower() == "отменен заказ 0 название1 автор1 2000 1250 издательство1 жанр1\n")

def test_refunded_unknown(shop):
    result = shop.process("Принять возврат заказа 0")
    assert (result.lower() == "не существует заказа 0")
