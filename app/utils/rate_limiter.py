from fastapi import HTTPException
import time
from app.config import settings


class RateLimiter:

    def __init__(self, calls: int, period: int):
        self.calls = calls
        self.period = period
        self.timestamps = []

    def __call__(self):
        now = time.time()
        self.timestamps = [t for t in self.timestamps if now - t < self.period]

        if len(self.timestamps) >= self.calls:
            raise HTTPException(
                status_code=429,
                detail="تم تجاوز حد الطلبات. يرجى المحاولة لاحقًا.")

        self.timestamps.append(now)


rate_limiter = RateLimiter(calls=settings.rate_limit_calls,
                           period=settings.rate_limit_period)
