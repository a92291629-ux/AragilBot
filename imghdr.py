# imghdr.py
import os

def what(file=None, h=None):
    """
    Replacement for deprecated imghdr.what function
    """
    if h is None:
        try:
            with open(file, 'rb') as f:
                h = f.read(32)
        except (OSError, TypeError):
            return None

    if not h:
        return None

    # Check for common image formats
    if h.startswith(b'\xff\xd8\xff'):
        return 'jpeg'
    if h.startswith(b'\x89PNG\r\n\x1a\n'):
        return 'png'
    if h.startswith(b'GIF87a') or h.startswith(b'GIF89a'):
        return 'gif'
    if h.startswith(b'BM'):
        return 'bmp'
    if h.startswith(b'RIFF') and len(h) >= 12 and h[8:12] == b'WEBP':
        return 'webp'
    if h.startswith(b'\x00\x00\x01\x00'):
        return 'ico'
    if h.startswith(b'\x49\x49\x2a\x00') or h.startswith(b'\x4d\x4d\x00\x2a'):
        return 'tiff'

    return None