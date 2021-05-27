from datetime import datetime
from shortuuid import ShortUUID

from django.utils.timezone import now, timedelta


def create_end_game_datetime() -> datetime:
    """Create datetime object pointing to 60 seconds later than now."""

    return now() + timedelta(seconds=60)

def create_short_uuid() -> str:
    """Create 6 length uuid. Unique for Lobby."""

    return ShortUUID().random(length=6).upper()
