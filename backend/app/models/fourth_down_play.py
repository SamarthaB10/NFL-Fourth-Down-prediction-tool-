import uuid

from sqlalchemy import Column, Date, Float, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID

from app.database import Base


class FourthDownPlay(Base):
    __tablename__ = "fourth_down_plays"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    season = Column(Integer)
    week = Column(Integer)
    game_id = Column(String)
    game_date = Column(Date)

    posteam = Column(String)
    defteam = Column(String)

    down = Column(Integer)
    ydstogo = Column(Integer)
    yardline_100 = Column(Float)
    qtr = Column(Integer)
    game_seconds_remaining = Column(Integer)
    score_differential = Column(Float)

    play_type = Column(String)
    decision = Column(String)
    yards_gained = Column(Integer)

    epa = Column(Float)
    wp = Column(Float)
    wpa = Column(Float)

    desc = Column(Text)


