from typing import Any, List

from sqlalchemy.orm.session import Session

from cinnamon_task_base.models.pipeline import JobModel
from cinnamon_task_base.repositories.base import BaseRepository


class JobRepository(BaseRepository):
    model_class = JobModel
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

    def find_by_unique_key(self, job_id: str) -> JobModel:
        return self.read_only_session.query(
            self.model_class).filter(self.model_class.job_id == job_id).one_or_none()

    def find_by_dag_id(self, dag_id: str) -> List[Any]:
        return self.read_only_session.query(
            self.model_class).filter(self.model_class.dag_id == dag_id)
