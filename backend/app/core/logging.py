import logging
import sys

def setup_logging(debug: bool = False) -> None:
    """Configure centralized logging for the application."""
    log_level = logging.DEBUG if debug else logging.INFO
    
    logging.basicConfig(
        stream=sys.stdout,
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    
    # Optional: Suppress overly verbose logs from third-party libraries here
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("asyncio").setLevel(logging.WARNING)
    
    # SQLAlchemy logging can be enabled for debug
    if not debug:
        logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
