import logging
import uvicorn
from config import config

if __name__ == "__main__":
    log_level = logging.INFO if config.APP_CONFIG.debug else logging.WARNING
    uvicorn.run("app.app:app", host="localhost", port=8050, log_level=log_level, workers=1)