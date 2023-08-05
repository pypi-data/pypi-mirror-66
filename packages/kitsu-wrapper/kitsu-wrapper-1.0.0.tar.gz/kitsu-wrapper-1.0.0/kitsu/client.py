from typing import *

import aiohttp

from .errors import *
from .models import *


class Client:
    def __init__(self):
        self._media = {"anime": Anime, "manga": Manga}
        self._base_url = 'https://kitsu.io/api/edge'
        self.__headers = {
            "Accept": "application/vnd.api+json",
            "Content-Type": "application/vnd.api+json"
        }

    async def search(self, type_: str, query: str, limit: int = 10) -> List[Union[Anime, Manga]]:
        media = self._media.get(type_)
        if media is None:
            raise InvalidArgument('You gave me an invalid media type! Supported media types: '
                                  + ', '.join(self._media.keys()))

        async with aiohttp.ClientSession(headers=self.__headers) as session:
            async with session.get(self._base_url + f'/{type_}?filter[text]={query}&page[limit]={limit}') as resp:
                if resp.status != 200:
                    raise ResponseError(code=resp.status, reason=resp.reason)

                json = await resp.json()

                return [media(type_, data) for data in json['data']]

    async def fetch_media_categories(self, media: Union[Anime, Manga]) -> List[Category]:
        if not isinstance(media, MediaEntry):
            raise InvalidArgument('You gave me an invalid media object! Supported media object types: '
                                  + ', '.join(c.__name__ for c in self._media.values()))

        async with aiohttp.ClientSession(headers=self.__headers) as session:
            async with session.get(self._base_url + f'/{media.type}/{media.id}/categories') as resp:
                if resp.status != 200:
                    raise ResponseError(code=resp.status, reason=resp.reason)

                json = await resp.json()

                return [Category(media.type, data) for data in json['data']]

    async def fetch_anime_streaming_links(self, anime: Anime) -> List[StreamingLink]:
        if not isinstance(anime, Anime):
            raise InvalidArgument('You gave me an invalid anime object!')

        async with aiohttp.ClientSession(headers=self.__headers) as session:
            async with session.get(self._base_url + f'/anime/{anime.id}/streaming-links') as resp:
                if resp.status != 200:
                    raise ResponseError(code=resp.status, reason=resp.reason)

                json = await resp.json()
                streaming_links = []

                for data in json['data']:
                    match = DOMAIN_NAME.match(data['attributes']['url'])
                    if match:
                        streaming_links.append(StreamingLink(data, match))

                return streaming_links
