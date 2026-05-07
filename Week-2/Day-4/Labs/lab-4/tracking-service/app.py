import os

from flask import Flask, jsonify, request

from database.db import InMemoryTrackingDB
from tracking.service import TrackingService

app = Flask(__name__)

db = InMemoryTrackingDB()
service = TrackingService(db=db)


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


@app.post("/tracking")
def create_tracking():
    """
    Create a tracking record.

    Body:
      { "tracking_id": "PKG123", "status": "IN_TRANSIT", "location": "BLR" }
    """
    data = request.get_json(silent=True) or {}
    tracking_id = (data.get("tracking_id") or "").strip()
    if not tracking_id:
        return jsonify({"error": "tracking_id is required"}), 400

    rec = service.create_or_update(
        tracking_id=tracking_id,
        status=(data.get("status") or "CREATED").strip(),
        location=(data.get("location") or "").strip() or None,
    )
    return jsonify(rec), 201


@app.get("/tracking/<tracking_id>")
def get_tracking(tracking_id: str):
    rec = service.get(tracking_id=tracking_id)
    if not rec:
        return jsonify({"error": "not found"}), 404
    return jsonify(rec)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "8000")), debug=True)

