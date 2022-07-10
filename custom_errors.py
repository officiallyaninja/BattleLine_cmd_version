class Error(Exception):
    ...


class CollectionFullError(Error):
    """Collection is full and cannot add new values"""
    ...


class SquadNotFullError(Error):
    """Squad is not full yet"""
    ...


class NoValidOptionsError(Error):
    """the input function can never terminate because there are no valid inputs the user can enter"""
    ...