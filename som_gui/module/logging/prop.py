class LoggingProperties:
    log_path: str = None
    log_format = "%(asctime)s | %(levelname)6s | %(module_func)50s [%(lineno)04d] |  %(message)s"
    log_level = None
    custom_formatter = None
