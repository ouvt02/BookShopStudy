'''Реализация книжного магазина'''
from dataclasses import dataclass


@dataclass
class Book:
    ''' Класс Книга'''
    title: str
    author: str
    year: str
    price: str
    publ_house: str
    genre: str


class Shop:
    '''Класс Магазин'''
    def __init__(self) -> None:
        self.catalog: list[Book] = []

    def process(self, cmd: str) -> str:
        '''Метод для обработки комманд'''
        if cmd.lower().startswith("добавить книгу"):
            self.add_book(cmd.lower().split("добавить книгу")[1])
            new_book = self.catalog[-1]
            message = f"Книга {new_book.title} {new_book.author} "
            message += f"{new_book.year} {new_book.price} "
            message += f"{new_book.publ_house} {new_book.genre} "
            message += "успешно добавлена\n"
            return message

        return f"Невозможно выполнить комманду '{cmd}'\n"

    def add_book(self, book_info: str) -> bool:
        '''Метод для добавления книги в каталог'''
        book = book_info.strip().split(' ')
        self.catalog.append(Book(book[0], book[1], book[2], book[3],
                                 book[4], book[5]))
        return True
