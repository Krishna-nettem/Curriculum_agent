import logging
import json
import traceback
from datetime import datetime
from typing import Any

class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        base: dict[str, Any] = {
            "timestamp": datetime.isoformat() + "Z",
            "level": record.levelname,
            "module": record.module,
            "message": record.getMessage()
        }
        if record.exc_info:
            base["exc_info"] = "".join(traceback.format_exception(*record.exc_info))

        for k, v in getattr(record, "extra_data", {}).items():
            base[k] = v
        return json.dumps(base, ensure_ascii=False)

def get_logger(logfile: str = "logs.json") -> logging.Logger:
    logger = logging.getLogger("course_creator")
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        fh = logging.FileHandler(logfile)
        fh.setLevel(logging.INFO)
        fh.setFormatter(JsonFormatter())
        logger.addHandler(fh)

        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        ch.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s"))
        logger.addHandler(ch)
    return logger
