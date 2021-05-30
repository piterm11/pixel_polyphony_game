from datetime import datetime
from shortuuid import ShortUUID
from typing import List

from django.db.models import QuerySet
from django.utils.timezone import now, timedelta


def create_start_game_datetime() -> datetime:
    """Create datetime object pointing to 10 seconds later than now."""
    return now() + timedelta(seconds=10)


def create_end_game_datetime() -> datetime:
    """Create datetime object pointing to 70 seconds later than now."""
    return now() + timedelta(seconds=70)


def create_short_uuid() -> str:
    """Create 6 length uuid. Unique for Lobby."""
    return ShortUUID().random(length=6).upper()


def create_list_of_hits(hit_list: QuerySet) -> List:
    """Create a json object containing a full list of hits in the game

    Each hit record contains instrument name and hit datetime.
    """
    new_hits_list = []
    for hit in hit_list:
        new_hits_list.append(
            {
                "instrument": hit.instrument.name,
                "tone": hit.tone,
                "datetime": hit.hit_date.isoformat(),
            }
        )
    return new_hits_list
