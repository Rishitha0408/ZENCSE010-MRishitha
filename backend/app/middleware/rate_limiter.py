"""
Rate Limiter Configuration

This module sets up 'SlowAPI', a rate-limiting tool that helps protect our 
server from being overwhelmed by too many requests (like spam or automated attacks).
"""

# 'Limiter' is the core class that tracks and restricts request frequency.
from slowapi import Limiter
# 'get_remote_address' is a utility that identifies users by their IP address 
# so we can apply limits to each person individually.
from slowapi.util import get_remote_address

# We initialize our limiter to track based on the visitor's IP address.
limiter = Limiter(key_func=get_remote_address)
