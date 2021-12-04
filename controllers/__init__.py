from flask import request, redirect, render_template

from common import get_db
from models import Task

__all__ = [
    'init_controllers',
]


def init_controllers(app):
    db = get_db()

    @app.route('/', methods=['POST', 'GET'])
    def index():
        if request.method == 'POST':
            task_content = request.form['content']
            new_task = Task(content=task_content)

            try:
                db.session.add(new_task)
                db.session.commit()
                return redirect('/')
            except:
                return 'There was an issue adding your task'

        else:
            tasks = Task.query.order_by(Task.date_created).all()
            return render_template('index.html', tasks=tasks)

    @app.route('/delete/<int:id>')
    def delete(id):
        task_to_delete = Task.query.get_or_404(id)

        try:
            db.session.delete(task_to_delete)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was a problem deleting that task'

    @app.route('/update/<int:id>', methods=['GET', 'POST'])
    def update(id):
        task = Task.query.get_or_404(id)

        if request.method == 'POST':
            task.content = request.form['content']

            try:
                db.session.commit()
                return redirect('/')
            except:
                return 'There was an issue updating your task'

        else:
            return render_template('update.html', task=task)

    @app.route('/done/<int:id>', methods=['GET', 'POST'])
    def done(id):
        task = Task.query.get_or_404(id)

        task.is_done = True

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'

    @app.route('/undone/<int:id>', methods=['GET', 'POST'])
    def undone(id):
        task = Task.query.get_or_404(id)

        task.is_done = False

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'
