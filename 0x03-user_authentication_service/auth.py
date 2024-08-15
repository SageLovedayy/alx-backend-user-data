#!/usr/bin/env python3

from bcrypt import hashpw, gensalt


def _hash_password(password: str) -> str:
    """Returns salted hashed password as bytestring"""
    return hashpw(password.encode("utf-8"), gensalt())
