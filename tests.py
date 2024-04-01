import pytest
from main import BooksCollector

class TestBooksCollector:
    def test_add_new_book_add_two_books(self):
        collector = BooksCollector()
        collector.add_new_book('Гордость и предубеждение и зомби')
        collector.add_new_book('Что делать, если ваш кот хочет вас убить')
        assert len(collector.get_books_genre()) == 2

    def test_add_new_book_add_one_books(self):
        collector = BooksCollector()
        collector.add_new_book('Путь война')
        assert len(collector.get_books_genre()) == 1

    def test_add_new_book_add_books_more_then_42_letters(self):
        collector = BooksCollector()
        collector.add_new_book('Путь война Путь война Путь война Путь война Путь война')
        assert collector.get_books_genre() == {}

    def test_add_new_book_add_books_with_0_letters(self):
        collector = BooksCollector()
        collector.add_new_book('')
        assert collector.get_books_genre() == {}

    def test_add_new_book_add_two_the_same_books(self):
        collector = BooksCollector()
        collector.add_new_book('Путь война')
        collector.add_new_book('Путь война')
        assert len(collector.get_books_genre()) == 1

    def test_books_for_children_no_adult_genre(self):
        collector = BooksCollector()
        collector.add_new_book('Гарри Потер')
        collector.add_new_book('Супер Ужасы')
        collector.add_new_book('Супер Детектив')
        collector.set_book_genre('Гарри Потер', 'Фантастика')
        collector.set_book_genre('Супер Ужасы', 'Ужасы')
        collector.set_book_genre('Супер Детектив', 'Детективы')

        children_books = collector.get_books_for_children()
        for book in children_books:
            assert collector.get_book_genre(book) not in collector.genre_age_rating

    def test_add_new_book_without_genre(self):
        collector = BooksCollector()
        collector.add_new_book('Некий тестовый том')
        assert collector.get_book_genre('Некий тестовый том') == ''

    def test_get_list_of_favorites_books(self):
        collector = BooksCollector()
        collector.add_new_book('Гарри Потер 1')
        collector.add_new_book('Гарри Потер 2')
        collector.add_new_book('Гарри Потер 3')
        collector.add_book_in_favorites('Гарри Потер 1')
        collector.add_book_in_favorites('Гарри Потер 3')

        favorites = collector.get_list_of_favorites_books()
        assert len(favorites) == 2
        assert 'Гарри Потер 1' in favorites
        assert 'Гарри Потер 2' not in favorites
        assert 'Гарри Потер 3' in favorites

    def test_delete_book_from_favorites(self):
        collector = BooksCollector()
        collector.add_new_book('Гарри Потер')
        collector.add_book_in_favorites('Гарри Потер')
        collector.delete_book_from_favorites('Гарри Потер')

        favorites = collector.get_list_of_favorites_books()
        assert 'Гарри Потер' not in favorites

    def test_delete_non_existing_book_from_favorites(self):
        collector = BooksCollector()
        collector.add_new_book('Я дом семья')
        collector.add_book_in_favorites('Я дом семья')
        collector.delete_book_from_favorites('Я люблю бегать')

        favorites = collector.get_list_of_favorites_books()
        assert 'Я дом семья' in favorites

    @pytest.mark.parametrize("books_in_favorites, book_to_delete, expected_favorites", [
        (['Гарри Потер 1'], 'Гарри Потер 1', []),
        (['Гарри Потер 1', 'Гарри Потер 2', 'Гарри Потер 3'], 'Гарри Потер 2', ['Гарри Потер 1', 'Гарри Потер 3']),
        (['Гарри Потер 1', 'Гарри Потер 2', 'Гарри Потер 3'], 'Дары смерти', ['Гарри Потер 1', 'Гарри Потер 2', 'Гарри Потер 3']),
    ])
    def test_delete_book_from_favorites_parametrized(self, books_in_favorites, book_to_delete, expected_favorites):
        collector = BooksCollector()
        for book in books_in_favorites:
            collector.add_new_book(book)
            collector.add_book_in_favorites(book)
        collector.delete_book_from_favorites(book_to_delete)

        favorites = collector.get_list_of_favorites_books()
        assert favorites == expected_favorites
