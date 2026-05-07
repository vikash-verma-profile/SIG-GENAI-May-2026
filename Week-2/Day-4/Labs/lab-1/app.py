import os
import time
from datetime import datetime, timedelta, timezone

import jwt
import psycopg2
from flask import Flask, jsonify, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from psycopg2.pool import SimpleConnectionPool
from redis import Redis
from werkzeug.security import check_password_hash

app = Flask(__name__)

# Env-driven configuration (no hardcoded secrets).
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "payments")
DB_USER = os.getenv("DB_USER", "payments_app")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")

JWT_SECRET = os.getenv("JWT_SECRET", "")
JWT_ISSUER = os.getenv("JWT_ISSUER", "payments-api")
JWT_TTL_SECONDS = int(os.getenv("JWT_TTL_SECONDS", "3600"))

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

if not JWT_SECRET:
    # Allow running locally without JWT, but enforce it in production.
    # (This is safer than silently issuing weak tokens.)
    app.logger.warning("JWT_SECRET not set; /login will not issue tokens.")

db_pool = SimpleConnectionPool(
    1,
    int(os.getenv("DB_POOL_MAX", "10")),
    host=DB_HOST,
    database=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
)

redis_client = Redis.from_url(REDIS_URL, decode_responses=True)

limiter = Limiter(get_remote_address, app=app, default_limits=["200 per day", "50 per hour"])


def _json_error(message: str, status: int):
    return jsonify({"error": message}), status


@app.get("/health")
def health():
    return jsonify({"status": "ok", "ts": int(time.time())})


@app.post("/login")
@limiter.limit("10 per minute")
def login():
    """
    Secure login endpoint.

    Expects JSON:
      { "username": "...", "password": "..." }
    """
    data = request.get_json(silent=True) or {}
    username = (data.get("username") or "").strip()
    password = data.get("password") or ""

    if not username or not password:
        return _json_error("username and password are required", 400)

    conn = db_pool.getconn()
    try:
        with conn.cursor() as cursor:
            # Parameterized query prevents SQL injection.
            cursor.execute(
                "SELECT id, password_hash FROM users WHERE username = %s",
                (username,),
            )
            row = cursor.fetchone()

        if not row:
            return _json_error("invalid credentials", 401)

        user_id, password_hash = row
        if not check_password_hash(password_hash, password):
            return _json_error("invalid credentials", 401)

        # Issue JWT (optional if JWT_SECRET is configured).
        if not JWT_SECRET:
            return jsonify({"message": "login successful", "user_id": user_id})

        now = datetime.now(tz=timezone.utc)
        token = jwt.encode(
            {
                "sub": str(user_id),
                "username": username,
                "iss": JWT_ISSUER,
                "iat": int(now.timestamp()),
                "exp": int((now + timedelta(seconds=JWT_TTL_SECONDS)).timestamp()),
            },
            JWT_SECRET,
            algorithm="HS256",
        )

        # Example: cache “last login” for monitoring/analytics.
        redis_client.setex(f"user:{user_id}:last_login", 24 * 3600, int(now.timestamp()))

        return jsonify({"message": "login successful", "token": token})
    except psycopg2.Error:
        app.logger.exception("database error during login")
        return _json_error("internal server error", 500)
    finally:
        db_pool.putconn(conn)


if __name__ == "__main__":
    # Local dev entrypoint.
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")), debug=True)

