from typing import Any, List

from cinnamon_task_base import Context
from cinnamon_task_base.log import logger

DATA_PATH = "data/"


@logger.class_logger
class BaseTask(object):
    ERROR_CODE_INTERNAL_SERVER_ERROR = 'INTERNAL_SERVER_ERROR'
    TASK_NAME = ''
    """
    Abstract task class.
    Please add your concrete code to concrete task class: `app/task.py`.
    """

    def __init__(self, context: Context) -> None:
        self.context = context
        self.set_arguments()
        self.logger.init_tasktime()

    def execute(self, inputs: List[Any]) -> List[Any]:
        pass

    def set_arguments(self) -> None:
        pass
