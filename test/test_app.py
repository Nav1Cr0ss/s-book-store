import pytest

from internal.app.book.book import BookApp
from internal.app.book.dto.book import BookSchema
from test.mock import BookRepoMock


# Just example how it should work
# The idea was to create easy-testable architecture without Monkey Patching
# For testing App layer we have to create mocks for repo and storage
# On current solution db and storage don't have interfaces
# storage="Background" - just placeholder to make it work

@pytest.mark.asyncio
async def test_get_books():
    book_app = BookApp(repo=BookRepoMock(), storage="Background")
    book: BookSchema = await book_app.get_book(1)
    assert book.id == 1
    assert book.title == "Sample Book"
