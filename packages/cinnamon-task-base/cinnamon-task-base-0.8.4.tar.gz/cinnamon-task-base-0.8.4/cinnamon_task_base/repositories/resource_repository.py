from typing import Any, List

from sqlalchemy.orm.session import Session

from cinnamon_task_base.models.pipeline import ResourceModel
from cinnamon_task_base.repositories.base import BaseRepository


class ResourceRepository(BaseRepository):
    model_class = ResourceModel
    RUNNING_STATUS = 'running'
    COMPLETE_STATUS = 'complete'

    @property
    def session(self) -> Session:
        return self.context.session

    @property
    def read_only_session(self) -> Session:
        return self.context.read_only_session

    def find_all(self) -> List[Any]:
        return self.read_only_session.query(self.model_class).all()

    def find_by_job_id(self, job_id: str) -> List[Any]:
        return self.read_only_session.query(
            self.model_class).filter(self.model_class.job_id == job_id)

    def find_by_unique_key(self, job_id: str, resource_id: str) -> ResourceModel:
        return self.read_only_session.query(self.model_class).filter(
            self.model_class.job_id == job_id,
            self.model_class.resource_id == resource_id).one_or_none()
