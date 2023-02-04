#!/usr/bin/env python3
"""Hashing passwords using bcrypt"""
import bcrypt


def hash_password(password: str) -> bytes:
    """Hashes password using bcrypt"""
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Checks if password maches with hashed password using bcrypt"""
    if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
        return True
    return False
