from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Optional, Protocol


@dataclass(frozen=True)
class TrackingRecord:
    tracking_id: str
    status: str
    location: Optional[str]


class TrackingDB(Protocol):
    def upsert(self, record: TrackingRecord) -> TrackingRecord: ...

    def get(self, tracking_id: str) -> Optional[TrackingRecord]: ...


class TrackingService:
    def __init__(self, db: TrackingDB):
        self._db = db

    def create_or_update(self, tracking_id: str, status: str, location: Optional[str]) -> dict:
        record = TrackingRecord(tracking_id=tracking_id, status=status, location=location)
        saved = self._db.upsert(record)
        return asdict(saved)

    def get(self, tracking_id: str) -> Optional[dict]:
        record = self._db.get(tracking_id)
        return asdict(record) if record else None

