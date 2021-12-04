from common import get_db

db = get_db()


class TaskList(db.Model):
    __tablename__ = 'task_lists'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.String, nullable=False)

    def __init__(self, description: str):
        self.description = description
