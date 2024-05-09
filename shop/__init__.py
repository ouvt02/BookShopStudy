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


# pylint: disable=too-many-instance-attributes
class Cart:
    '''Класс Корзина'''
    def __init__(self, cart_id: int) -> None:
        self.cart_id: int = cart_id
        self.books: list[Book] = []
        self.in_delivery = False
        self.in_refund = False
        self.delivery_address = ""
        self.delivery_time = ""
        self.delivery_pay_way = ""
        self.delivered = False
        self.refunded = False

    def delivery(self, delivery_info: str) -> bool:
        '''Метод для оформления доставки'''
        delivery = delivery_info.split(' ')

        self.in_delivery = True
        self.delivery_address = delivery[0]
        self.delivery_time = delivery[1]
        self.delivery_pay_way = delivery[2]

        return True

    def refund(self, refund: list[str]) -> bool:
        '''Метод для отмены доставки'''
        self.in_delivery = False
        self.in_refund = True

        self.delivery_pay_way = refund[1]
        self.delivery_address = refund[2]
        self.delivery_time = refund[3]

        return True


class Shop:
    '''Класс Магазин'''
    def __init__(self) -> None:
        self.catalog: list[Book] = []
        self.carts_counter: int = 0
        self.carts: dict[int, Cart] = {}
        self.orders: dict[int, int] = {}
        self.orders_counter = 0

    # pylint: disable=too-many-branches
    # pylint: disable=too-many-statements
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

        elif cmd.lower().startswith("оформить заказ"):
            order_info = cmd.lower().split("оформить заказ")[1]
            if self.delivery(order_info.strip()):
                result = f"Заказ {self.orders_counter - 1} "
                result += "оформлен "
                cart = self.carts[self.carts_counter - 1]
                result += f"{cart.delivery_address} "
                result += f"{cart.delivery_time} "
                result += f"{cart.delivery_pay_way}\n"
            else:
                result = "Корзина пуста\n"

        elif cmd.lower().startswith("отменить заказ"):
            refund_info = cmd.lower().split("отменить заказ")[1]
            if self.refund(refund_info.strip()):
                cart_num = self.orders[int(refund_info.strip()[0])]
                out = f"Заказ {int(refund_info.strip()[0])} отменен "
                out += f"{self.carts[cart_num].delivery_pay_way} "
                out += f"{self.carts[cart_num].delivery_address} "
                out += f"{self.carts[cart_num].delivery_time}: "
                for book in self.carts[cart_num].books:
                    out += f"{book.title} {book.author} {book.year} "
                    out += f"{book.price} {book.publ_house} {book.genre}\n"
                del self.orders[int(refund_info.strip()[0])]
                self.orders_counter -= 1
                result = out
            else:
                result = "Не существует заказа\n"

        elif cmd.lower().startswith("доставить заказ"):
            order_num = int((cmd.lower().split("доставить заказ")[1]).strip())
            out = f"Доставлен заказ {order_num} "
            if self.deliver(order_num):
                for book in self.carts[order_num].books:
                    out += f"{book.title} {book.author} {book.year} "
                    out += f"{book.price} {book.publ_house} {book.genre}\n"
                result = out
            else:
                result = f"Не существует заказа {order_num}"

        elif cmd.lower().startswith("принять возврат заказа"):
            order_info = cmd.lower().split("принять возврат заказа")[1]
            order_info = order_info.strip()
            order_num = int(order_info)
            out = f"Отменен заказ {order_num} "
            if self.cancel(order_num):
                for book in self.carts[order_num].books:
                    out += f"{book.title} {book.author} {book.year} "
                    out += f"{book.price} {book.publ_house} {book.genre}\n"
                result = out
            else:
                result = f"Не существует заказа {order_num}"

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

        if (self.carts_counter == 0 or
                self.carts[self.carts_counter - 1].in_delivery):
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

    def delivery(self, delivery_info: str) -> bool:
        '''Метод для оформления доставки'''
        if (self.carts_counter == 0 or
                self.carts[self.carts_counter - 1].in_delivery):
            return False

        result = self.carts[self.carts_counter - 1].delivery(delivery_info)
        self.orders[self.orders_counter] = self.carts_counter - 1
        self.orders_counter += 1

        return result

    def refund(self, refund_info: str) -> bool:
        '''Метод для отмены доставки'''
        refund = refund_info.split(' ')
        order_num = int(refund[0])

        if (self.carts_counter == 0 or order_num not in self.carts or
                self.carts[order_num].in_refund):
            return False

        return self.carts[order_num].refund(refund)

    def deliver(self, order_num: int) -> bool:
        '''Метод для доставки заказа'''
        # pylint: disable=too-many-boolean-expressions
        if (self.carts_counter == 0 or order_num not in self.carts or
                not self.carts[order_num].in_delivery or
                self.carts[order_num].in_refund or
                self.carts[order_num].refunded or
                self.carts[order_num].delivered):
            return False

        self.carts[order_num].delivered = True
        self.carts[order_num].in_delivery = False

        return True

    def cancel(self, order_num: int) -> bool:
        '''Метод для отмены заказа'''
        # pylint: disable=too-many-boolean-expressions
        if (self.carts_counter == 0 or order_num not in self.carts or
                self.carts[order_num].in_delivery or
                not self.carts[order_num].in_refund or
                self.carts[order_num].refunded or
                self.carts[order_num].delivered):
            return False

        self.carts[order_num].refunded = True
        self.carts[order_num].in_refund = False

        return True
