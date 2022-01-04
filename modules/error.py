error_hierarchy = {
    "BaseError": {
    }
}


class BaseError(Exception):
    pass


class TransactionsQueryError(BaseError):
    pass


__all__ = [
    "error_hierarchy",
    "BaseError",
    "TransactionsQueryError"
]
