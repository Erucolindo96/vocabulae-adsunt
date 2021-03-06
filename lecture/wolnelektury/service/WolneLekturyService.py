import gc
import logging

from database.dao.AgeDao import AgeDao
from database.dao.BookDao import BookDao
from database.entities.Age import Age
from database.entities.Book import Book
from lecture.wolnelektury.service.LectureListLoader import LectureListLoader, LectureTranslatedException
from lecture.wolnelektury.service.TextPreprocessing import TextPreprocessing


class WolneLekturyService:

    @staticmethod
    def load_lecture_by_author_slug(a: str) -> None:
        l_list = LectureListLoader.list_by_author_slug(a)

        for l in l_list:
            try:
                href = l['href']
                details = LectureListLoader.get_details(href)
                LectureListLoader.check_is_polish(details)

                age = LectureListLoader.create_age(details)

                content = LectureListLoader.get_content(details)
                if content is not None:
                    preprocessed_content = WolneLekturyService.__preprocess_content(content)
                    content_in_str = " ".join(preprocessed_content)
                    book = LectureListLoader.create_book(details=details,
                                                         content=content_in_str, href=href)
                    WolneLekturyService.__save_book_in_database(book=book, age=age)
                    del content
                    del preprocessed_content
                    del content_in_str
            except LectureTranslatedException as e:
                logging.info(
                    'Książka {} autora {} jest tłumaczeniem, z polskiego na język obcy, albo w drugą stronę'.format(
                        e.get_lecture(), a))
            except:
                logging.exception("Nieznany wyjątek podczas ściągania {} autora {}",
                                  l['title'], a)
        gc.collect()

    @staticmethod
    def __preprocess_content(content: str):
        content = TextPreprocessing.remove_author_and_title(content)
        word_list = LectureListLoader.get_text_only_from_lecture(content)
        return TextPreprocessing.to_lemmas(word_list)

    @staticmethod
    def __save_book_in_database(book: Book, age: Age):
        age_dao = AgeDao()

        exist_age = age_dao.get_by_slug(age.get_slug())
        if exist_age is not None:
            book.set_age(exist_age)
        else:
            age_dao.insert(age_name=age.get_name(), age_slug=age.get_slug())
            saved_age = age_dao.get_by_slug(age.get_slug())
            book.set_age(saved_age)
        book_dao = BookDao()
        book_dao.insert(book)
