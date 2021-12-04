from datetime import datetime

from common import get_db

db = get_db()


class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    is_done = db.Column(db.Boolean, default=False)

    def __init__(self, content, is_done=False):
        self.content = content
        self.is_done = is_done

    def __repr__(self):
        return f'{self.date_created.isoformat()} | {self.content} | {"❌" if not self.is_done else "✅"}'
