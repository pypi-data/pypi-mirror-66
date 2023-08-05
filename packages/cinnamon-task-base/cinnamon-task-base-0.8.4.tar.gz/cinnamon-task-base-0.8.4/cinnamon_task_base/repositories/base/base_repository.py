from typing import Dict, List, Union

from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.orm.session import Session

from cinnamon_task_base.context import Context


class BaseRepository(object):
    model_class = DeclarativeMeta

    @property
    def session(self) -> Session:
        raise Exception('Not Implements of session. Please override.')

    @property
    def read_only_session(self) -> Session:
        raise Exception('Not Implements of read_only_session. Please override.')

    def __init__(self, context: Context) -> None:
        self.context = context

    def all(self) -> List[DeclarativeMeta]:
        objects = self.read_only_session.query(self.model_class).all()
        self.session.commit()
        return objects

    def create(self, fields: Dict) -> DeclarativeMeta:
        try:
            model = self.model_class(**fields)
            model = self.session.merge(model)
            self.session.add(model)
            self.session.commit()
        except:
            self.session.rollback()
            raise

        return model

    def update(self, model: DeclarativeMeta, fields: Dict) -> DeclarativeMeta:
        try:
            for key in fields:
                setattr(model, key, fields[key])
            model = self.session.merge(model)
            self.session.add(model)
            self.session.commit()
        except:
            self.session.rollback()
            raise

        return model

    def delete(self, model: DeclarativeMeta) -> None:
        try:
            model = self.session.merge(model)
            self.session.delete(model)
            self.session.commit()
        except:
            self.session.rollback()
            raise

    def find(self, primary_id: int) -> DeclarativeMeta:
        return self.read_only_session.query(
            self.model_class).filter(self.model_class.id == primary_id).one_or_none()

    def exist(self, primary_id: Union[int, str]) -> bool:
        return self.read_only_session.query(
            self.model_class).filter(self.model_class.id == primary_id).exists().scalar()

    def save(self) -> None:
        self.session.commit()
