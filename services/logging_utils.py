from logging import getLogger

success_logger = getLogger('success')
warning_logger = getLogger('warning')
error_logger = getLogger('error')

def log_success(message: str) -> None:
    success_logger.info(message)

def log_warning(message: str) -> None:
    warning_logger.warning(message)

def log_error(message: str) -> None:
    error_logger.error(message)