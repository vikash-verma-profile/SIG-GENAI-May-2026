from __future__ import annotations

from typing import Dict, Optional

from tracking.service import TrackingRecord


class InMemoryTrackingDB:
    def __init__(self):
        self._data: Dict[str, TrackingRecord] = {}

    def upsert(self, record: TrackingRecord) -> TrackingRecord:
        self._data[record.tracking_id] = record
        return record

    def get(self, tracking_id: str) -> Optional[TrackingRecord]:
        return self._data.get(tracking_id)

