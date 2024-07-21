from loguru import logger
import sys

logger.add(sys.stdout, format="{time} {level} {message}", level="DEBUG")
