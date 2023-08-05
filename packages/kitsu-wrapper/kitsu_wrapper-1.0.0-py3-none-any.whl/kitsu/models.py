import re
from datetime import datetime


__all__ = ('DOMAIN_NAME', 'StreamingLink', 'Category', 'MediaEntry', 'Anime', 'Manga')

DOMAIN_NAME = re.compile('^(?:https?://)?(?:[a-zA-Z0-9]{1,63}\.)*([a-zA-Z0-9]{1,63})\.(?:[a-zA-Z0-9]{1,63})/')
CUSTOM_STREAMERS_NAMES = {
    "hidive": "HIDIVE",
    "tubitv": "TubiTV",
    "youtube": "YouTube"
}


class StreamingLink:
    __slots__ = ('id', 'url', 'subs', 'dubs', 'title')

    def __init__(self, data: dict, match: re.Match):
        attributes = data['attributes']

        self.id = data['id']
        self.url = attributes['url']
        self.subs = attributes['subs']
        self.dubs = attributes['dubs']

        domain_name = match.group(1)
        self.title = CUSTOM_STREAMERS_NAMES.get(domain_name, domain_name.title())

    def __str__(self):
        return self.title


class Category:
    __slots__ = ('id', 'type', 'title', 'description', 'slug', 'nsfw', 'media_count', 'child_count', 'image_url')

    def __init__(self, type_, data: dict):
        attributes = data['attributes']

        self.id = data['id']
        self.type = type_
        self.title = attributes['title']
        self.description = attributes['description']
        self.slug = attributes['slug']
        self.nsfw = attributes['nsfw']
        self.media_count = attributes['totalMediaCount']
        self.child_count = attributes['childCount']
        self.image_url = attributes['image']['original'] \
            if attributes['image'] else None

    @property
    def url(self) -> str:
        return f'https://kitsu.io/explore/{self.type}/category/{self.slug}'

    def __str__(self):
        return self.title


class MediaEntry:
    __slots__ = ('id', 'type', 'title', 'synopsis', 'subtype', 'status', 'slug', 'average_rating', 'user_count',
                 'favorites_count', 'popularity_rank', 'rating_rank', 'age_rating', 'age_rating_guide',
                 'poster_image_url', 'cover_image_url', 'started_at', 'ended_at', 'next_release')

    def __init__(self, id_: str, type_: str, attributes: dict):
        self.id = id_
        self.type = type_
        self.title = attributes['canonicalTitle']
        self.synopsis = attributes['synopsis']
        self.subtype = attributes['subtype']
        self.status = attributes['status']
        self.slug = attributes['slug']
        self.average_rating = attributes['averageRating']
        self.user_count = attributes['userCount']
        self.favorites_count = attributes['favoritesCount']
        self.popularity_rank = attributes['popularityRank']
        self.rating_rank = attributes['ratingRank']
        self.age_rating = attributes['ageRating']
        self.age_rating_guide = attributes['ageRatingGuide']
        self.poster_image_url = attributes['posterImage']['original'] \
            if attributes['posterImage'] else None
        self.cover_image_url = attributes['coverImage']['original'] \
            if attributes['coverImage'] else None
        self.started_at = datetime.strptime(attributes['startDate'], '%Y-%m-%d') \
            if attributes['startDate'] else None
        self.ended_at = datetime.strptime(attributes['endDate'], '%Y-%m-%d') \
            if attributes['endDate'] else None
        self.next_release = datetime.strptime(attributes['nextRelease'], '%Y-%m-%dT%H:%M:%S.%f+09:00') \
            if attributes['nextRelease'] else None

    @property
    def url(self) -> str:
        return f'https://kitsu.io/{self.type}/{self.slug}'

    def __str__(self):
        return self.title


class Anime(MediaEntry):
    __slots__ = ('id', 'type', 'title', 'synopsis', 'subtype', 'status', 'slug', 'average_rating', 'user_count',
                 'favorites_count', 'popularity_rank', 'rating_rank', 'age_rating', 'age_rating_guide',
                 'poster_image_url', 'cover_image_url', 'started_at', 'ended_at', 'next_release',
                 'episode_count', 'episode_length', 'total_length', 'youtube_video_id', 'nsfw')

    def __init__(self, type_: str, data: dict):
        attributes = data['attributes']

        super().__init__(data['id'], type_, attributes)

        self.episode_count = attributes['episodeCount']
        self.episode_length = attributes['episodeLength']
        self.total_length = attributes['totalLength']
        self.youtube_video_id = attributes['youtubeVideoId']
        self.nsfw = attributes['nsfw']


class Manga(MediaEntry):
    __slots__ = ('id', 'type', 'title', 'synopsis', 'subtype', 'status', 'slug', 'average_rating', 'user_count',
                 'favorites_count', 'popularity_rank', 'rating_rank', 'age_rating', 'age_rating_guide',
                 'poster_image_url', 'cover_image_url', 'started_at', 'ended_at', 'next_release',
                 'chapter_count', 'volume_count', 'serialization')

    def __init__(self, type_: str, data: dict):
        attributes = data['attributes']

        super().__init__(data['id'], type_, attributes)

        self.chapter_count = attributes['chapterCount']
        self.volume_count = attributes['volumeCount']
        self.serialization = attributes['serialization']
