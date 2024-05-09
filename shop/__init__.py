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


# pylint: disable=too-few-public-methods
class Cart:
    '''Класс Корзина'''
    def __init__(self, cart_id: int) -> None:
        self.cart_id: int = cart_id
        self.books: list[Book] = []


class Shop:
    '''Класс Магазин'''
    def __init__(self) -> None:
        self.catalog: list[Book] = []
        self.carts_counter: int = 0
        self.carts: dict[int, Cart] = {}

    def process(self, cmd: str) -> str:
        '''Метод для обработки комманд'''
        result = f"Невозможно выполнить комманду '{cmd}'\n"
        if cmd.lower().startswith("добавить книгу"):
            self.add_book(cmd.lower().split("добавить книгу")[1])
            new_book = self.catalog[-1]
            message = f"Книга {new_book.title} {new_book.author} "
            message += f"{new_book.year} {new_book.price} "
            message += f"{new_book.publ_house} {new_book.genre} "
            message += "успешно добавлена\n"
            result = message

        elif cmd.lower().startswith("просмотреть каталог"):
            out = ""
            for book in self.catalog:
                out += f"{book.title} {book.author} {book.year} {book.price} "
                out += f"{book.publ_house} {book.genre}\n"
            result = out

        elif cmd.lower().startswith("положить в корзину книгу"):
            book_title = cmd.lower().split("положить в корзину книгу")[1]
            book_title = book_title.strip()
            if self.add_book_to_cart(book_title):
                result = f"Книга {book_title} успешно добавлена в корзину"
            else:
                result = f"Книги {book_title} нет в каталоге"

        elif cmd.lower().startswith("удалить из корзины"):
            book_title = (cmd.lower().split("удалить из корзины")[1]).strip()
            if self.delete_from_cart(book_title):
                result = f"Книга {book_title} успешно удалена из корзины"
            else:
                result = f"Книги {book_title} нет в корзине"

        elif cmd.lower().startswith("просмотреть содержимое корзины"):
            out = ""
            if self.carts_counter != 0:
                for book in self.carts[self.carts_counter - 1].books:
                    out += f"{book.title} {book.author} {book.year} "
                    out += f"{book.price} {book.publ_house} {book.genre}\n"
            result = out

        return result

    def add_book(self, book_info: str) -> bool:
        '''Метод для добавления книги в каталог'''
        book = book_info.strip().split(' ')
        self.catalog.append(Book(book[0], book[1], book[2], book[3],
                                 book[4], book[5]))
        return True

    def add_book_to_cart(self, book_title: str) -> bool:
        '''Метод для добавления книги в корзину'''
        book_to_cart = None
        for book in self.catalog:
            if book.title == book_title:
                book_to_cart = book
                break

        if book_to_cart is None:
            return False

        if self.carts_counter == 0:
            self.carts[self.carts_counter] = Cart(self.carts_counter)
            self.carts[self.carts_counter].books.append(book_to_cart)
            self.carts_counter += 1
        else:
            self.carts[self.carts_counter - 1].books.append(book_to_cart)

        return True

    def delete_from_cart(self, book_title: str) -> bool:
        '''Метод для удаления книги из корзины'''
        book_title = book_title.strip()
        book_to_delete = None

        if self.carts_counter == 0:
            return False

        for book in self.carts[self.carts_counter - 1].books:
            if book.title == book_title:
                book_to_delete = book
                self.carts[self.carts_counter - 1].books.remove(book_to_delete)
                break

        if book_to_delete is None:
            return False

        return True
