import logging
from django.dispatch import Signal, receiver

user_blocked_signal = Signal()
logger = logging.getLogger(__name__)


@receiver(user_blocked_signal)
def log_user_blocked(sender, **kwargs):
    email = kwargs.get("email")
    block_time = kwargs.get("block_time")
    logger.warning(f"Email {email} has been blocked for {block_time} seconds.")
