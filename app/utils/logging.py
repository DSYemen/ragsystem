import logging
from app.config import settings

def setup_logger():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        filename=settings.log_file,
        filemode='a'
    )
    return logging.getLogger(__name__)

logger = setup_logger()