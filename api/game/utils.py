from datetime import datetime
from shortuuid import ShortUUID

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
