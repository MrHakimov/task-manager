from sqlalchemy import func

from common import get_db

from .task_list import TaskList

db = get_db()


class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String, nullable=False)
    date_created = db.Column(db.DateTime, server_default=func.now())
    is_done = db.Column(db.Boolean, server_default='f')
    task_list_id = db.Column(db.Integer, db.ForeignKey(TaskList.id), nullable=False)

    def __init__(self, content, task_list_id, is_done=False):
        self.content = content
        self.task_list_id = task_list_id
        self.is_done = is_done

    def __repr__(self):
        return f'{self.date_created.isoformat()} | {self.content} | {"❌" if not self.is_done else "✅"}'
