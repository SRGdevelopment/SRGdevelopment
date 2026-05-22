from sqlalchemy import Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Market(Base):
    __tablename__ = "markets"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    event: Mapped[str] = mapped_column(String, index=True)
    side_a_price_cents: Mapped[int] = mapped_column(Integer)
    side_b_price_cents: Mapped[int] = mapped_column(Integer)
    liquidity: Mapped[float] = mapped_column(Float, default=0.5)
    volatility: Mapped[float] = mapped_column(Float, default=0.2)
    is_live: Mapped[int] = mapped_column(Integer, default=1)
