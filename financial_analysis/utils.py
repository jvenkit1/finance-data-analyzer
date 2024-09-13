import logging


def handle_api_errors(func):
    """Decorator to handle API errors gracefully and log them."""

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError as e:
            logging.error(f"KeyError in function '{func.__name__}': {e}")
            return None
        except ValueError as e:
            logging.error(f"ValueError in function '{func.__name__}': {e}")
            return None
        except Exception as e:
            logging.error(f"An error occurred in function '{func.__name__}': {e}")
            return None

    return wrapper
