import logging
from pathlib import Path

from datetime import datetime


LOG_PATH = Path("logs")

LOG_PATH.mkdir(exist_ok=True)

# 每次运行生成独立日志文件，避免 Windows 下多次运行对同一文件加锁冲突
RUN_STAMP = datetime.now().strftime(
    "%Y%m%d_%H%M%S"
)

LOG_FILE = LOG_PATH / f"test_{RUN_STAMP}.log"

# 即便日志文件写入失败（如权限 / 占用），也绝不影响测试执行
logging.raiseExceptions = False


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(
            LOG_FILE,
            encoding="utf-8",
            delay=True
        ),
        logging.StreamHandler()
    ]
)


logger = logging.getLogger(__name__)