from pkg.storage.google_bucket.storage import Storage, Bucket
from settings import config


class BucketBooks(Bucket):
    name = config.Storage.BUCKED_BOOKS


class StorageBook(Storage):
    bucket = BucketBooks

    async def upload_book(self, file_bytes: bytes, file_name: str) -> str:
        return await self._upload_file_by_bytes(file_bytes, file_name)

    async def download_book(self, file_name: str) -> bytes:
        return await self._download_file_to_bytes(file_name)
