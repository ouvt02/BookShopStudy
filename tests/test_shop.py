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
