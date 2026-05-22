import structlog
import logging
from datetime import datetime
from pathlib import Path

# Setup Structlog (lebih rapi dari print biasa)
structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer()
    ]
)

logger = structlog.get_logger()

class AppLogger:
    def __init__(self):
        self.log_dir = Path("logs")
        self.log_dir.mkdir(exist_ok=True)
        
        self.setup_file_logging()

    def setup_file_logging(self):
        log_file = self.log_dir / f"app_{datetime.now().strftime('%Y%m%d')}.log"
        
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setLevel(logging.INFO)
        
        logging.basicConfig(
            level=logging.INFO,
            handlers=[file_handler]
        )

    def log_interaction(self, user_id: str, action: str, details: dict = None):
        logger.info("chat_interaction", 
                   user_id=user_id,
                   action=action,
                   timestamp=datetime.now().isoformat(),
                   **(details or {}))

    def log_error(self, error: Exception, context: str = ""):
        logger.error("error_occurred", 
                    error=str(error),
                    context=context,
                    timestamp=datetime.now().isoformat())