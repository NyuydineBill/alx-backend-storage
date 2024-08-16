#!/usr/bin/env python3
"""
Web cache and URL access tracker using Redis.
"""

import requests
import redis
from typing import Callable


class Cache:
    """Cache class to interact with Redis."""

    def __init__(self):
        """Initialize the connection to the Redis server."""
        self._redis = redis.Redis()

    def get_page(self, url: str) -> str:
        """
        Get the HTML content of a URL, track access count, and cache with expiration.
        
        Args:
            url (str): The URL to fetch.
        
        Returns:
            str: The HTML content of the URL.
        """
        cache_key = f"count:{url}"
        self._redis.incr(cache_key)
        
        cached_page = self._redis.get(url)
        if cached_page:
            return cached_page.decode('utf-8')
        
        response = requests.get(url)
        page_content = response.text
        
        self._redis.setex(url, 10, page_content)
        return page_content

    def get_count(self, url: str) -> int:
        """
        Get the access count of a URL.
        
        Args:
            url (str): The URL to get the count for.
        
        Returns:
            int: The access count.
        """
        count = self._redis.get(f"count:{url}")
        return int(count) if count else 0


if __name__ == "__main__":
    cache = Cache()

    url = "http://slowwly.robertomurray.co.uk"
    print(cache.get_page(url))
    print(f"URL accessed {cache.get_count(url)} times")

