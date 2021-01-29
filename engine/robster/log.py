import logging
import os


DEBUG = os.environ.get("ROBSTER_PRODUCTION", None) == None


logger = logging.getLogger("robster")
logger.setLevel(logging.DEBUG if DEBUG else logging.INFO)
formatter = logging.Formatter("[%(asctime)s|%(levelname)s] %(message)s")
handlers = [
    logging.StreamHandler(),
]

if DEBUG:
    handlers.append(logging.FileHandler("robster-debug.log"))

for handler in handlers:
    handler.setFormatter(formatter)
    logger.addHandler(handler)
