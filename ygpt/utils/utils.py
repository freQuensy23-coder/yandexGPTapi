def try_or_none(f):
    """Try to execute function and return None if it fails."""
    try:
        return f()
    except:
        return None
