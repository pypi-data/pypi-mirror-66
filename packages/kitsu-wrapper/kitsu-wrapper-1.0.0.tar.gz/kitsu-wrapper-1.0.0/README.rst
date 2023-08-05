|Disco|
-------

|Discord| |License| |Twitter|

kitsu-wrapper
=============

A simple python async wrapper for the Kitsu.io API.

Supports searches for Animes, Mangas and Streaming Links.

Installation
------------

**NOTE**: Python 3.6 or higher is required.

.. code:: python

   # Windows
   py -3.6 -m pip install kitsu-wrapper

   # Linux
   python3.6 -m pip install kitsu-wrapper

Example
-------

.. code:: python

   import asyncio

   import kitsu


   client = kitsu.Client()


   async def anime_search(query):
       entries = await client.search('anime', query, limit=5)
       if not entries:
           print(f'No entries found for "{query}"')
           return

       for i, anime in enumerate(entries, 1):
           print(f'\n{i}. {anime.title}:')
           print('---> Sub-Type:', anime.subtype)
           print('---> Status:', anime.status)
           print('---> Synopsis:\n' + anime.synopsis)
           print('---> Episodes:', anime.episode_count)
           print('---> Age Rating:', anime.age_rating_guide)
           print('---> Ranking:')
           print('-> Popularity:', anime.popularity_rank)
           print('-> Rating:', anime.rating_rank)

           if anime.started_at:
               print('---> Started At:', anime.started_at.strftime('%Y-%m-%d'))
           if anime.ended_at:
               print('---> Ended At:', anime.ended_at.strftime('%Y-%m-%d'))

           streaming_links = await client.fetch_anime_streaming_links(anime)
           if streaming_links:
               print('---> Streaming Links:')
               for link in streaming_links:
                   print(f'-> {link.title}: {link.url}')

           print('---> Kitsu Page:', anime.url)


   async def manga_search(query):
       entries = await client.search('manga', query, limit=5)
       if not entries:
           print(f'No entries found for "{query}"')
           return

       for i, manga in enumerate(entries, 1):
           print(f'\n{i}. {manga.title}:')
           print('---> Sub-Type:', manga.subtype)
           print('---> Status:', manga.status)
           print('---> Volumes:', manga.volume_count)
           print('---> Chapters:', manga.chapter_count)
           print('---> Synopsis:\n' + manga.synopsis)
           print('---> Age Rating:', manga.age_rating_guide)
           print('---> Ranking:')
           print('-> Popularity:', manga.popularity_rank)
           print('-> Rating:', manga.rating_rank)

           if manga.started_at:
               print('---> Started At:', manga.started_at.strftime('%Y-%m-%d'))
           if manga.ended_at:
               print('---> Ended At:', manga.ended_at.strftime('%Y-%m-%d'))

           print('---> Kitsu Page:', manga.url)


   loop = asyncio.get_event_loop()
   loop.run_until_complete(anime_search(input('Insert an anime name: ')))
   loop.run_until_complete(manga_search(input('Insert a manga name: ')))


.. |Disco| image:: https://i.imgur.com/DWa6iY0.png
   :target: https://is.gd/disco_github
.. |Discord| image:: https://img.shields.io/discord/516346444463210542?label=chat&logo=discord
   :target: https://discord.gg/qN5886E
.. |License| image:: https://img.shields.io/github/license/DiscoMusic/kitsu-wrapper
   :target: https://github.com/DiscoMusic/kitsu-wrapper/tree/master/LICENSE
.. |Twitter| image:: https://img.shields.io/twitter/follow/DiscoTheBot
   :target: https://twitter.com/DiscoTheBot