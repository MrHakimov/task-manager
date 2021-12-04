from flask import request, redirect, render_template

from common import get_db
from models import Task, TaskList

__all__ = [
    'init_controllers',
]


def init_controllers(app):
    db = get_db()

    @app.route('/', methods=['POST', 'GET'])
    @app.route('/lists', methods=['POST', 'GET'])
    def index():
        if request.method == 'POST':
            description = request.form['content']
            if description == '':
                return 'List name should not be empty'

            new_list = TaskList(description=description)

            try:
                db.session.add(new_list)
                db.session.commit()
                return redirect('/')
            except:
                return 'There was an issue creating your list'

        else:
            lists = TaskList.query.all()
            return render_template('index.html', lists=lists)

    @app.route('/lists/<int:list_id>/', methods=['POST', 'GET'])
    def create_task(list_id: int):
        if request.method == 'POST':
            task_content = request.form['content']
            if task_content == '':
                return 'Task content should not be empty'

            new_task = Task(content=task_content, task_list_id=list_id)

            try:
                db.session.add(new_task)
                db.session.commit()
                return redirect(f'/lists/{list_id}')
            except:
                return 'There was an issue adding your task'
        else:
            _list_id = TaskList.query.where(TaskList.id == list_id).first()

            if _list_id is None:
                return redirect('/')

            tasks = Task.query.where(Task.task_list_id == list_id).order_by(Task.date_created).all()
            task_list_id = list_id
            return render_template('list_tasks.html', tasks=tasks, task_list_id=task_list_id)

    @app.route('/lists/<int:list_id>/delete/<int:task_id>')
    def delete_task(list_id, task_id):
        task_to_delete = Task.query.get_or_404(task_id)

        try:
            db.session.delete(task_to_delete)
            db.session.commit()
            return redirect(f'/lists/{list_id}')
        except:
            return 'There was a problem deleting that task'

    @app.route('/lists/<int:list_id>/update/<int:task_id>', methods=['GET', 'POST'])
    def update_task(list_id, task_id):
        task = Task.query.get_or_404(task_id)

        if request.method == 'POST':
            task.content = request.form['content']

            try:
                db.session.commit()
                return redirect(f'/lists/{list_id}')
            except:
                return 'There was an issue updating your task'

        else:
            return render_template('task_update.html', task=task)

    @app.route('/lists/<int:list_id>/done/<int:task_id>', methods=['GET', 'POST'])
    def done_task(list_id, task_id):
        task = Task.query.get_or_404(task_id)

        task.is_done = True

        try:
            db.session.commit()
            return redirect(f'/lists/{list_id}')
        except:
            return 'There was an issue updating your task'

    @app.route('/lists/<int:list_id>/undone/<int:task_id>', methods=['GET', 'POST'])
    def undone_task(list_id, task_id):
        task = Task.query.get_or_404(task_id)

        task.is_done = False

        try:
            db.session.commit()
            return redirect(f'/lists/{list_id}')
        except:
            return 'There was an issue updating your task'

    @app.route('/lists/<int:list_id>/rename', methods=['GET', 'POST'])
    def rename_list(list_id):
        task_list = TaskList.query.get_or_404(list_id)

        if request.method == 'POST':
            task_list.description = request.form['content']

            try:
                db.session.commit()
                return redirect(f'/lists')
            except:
                return 'There was an issue renaming your list'

        else:
            return render_template('list_rename.html', list=task_list)

    @app.route('/lists/<int:list_id>/delete')
    def delete_list(list_id):
        tasks_to_delete = Task.query.where(Task.task_list_id == list_id).all()
        list_to_delete = TaskList.query.get_or_404(list_id)

        try:
            for task in tasks_to_delete:
                db.session.delete(task)
            db.session.delete(list_to_delete)
            db.session.commit()
            return redirect('/lists')
        except:
            return 'There was a problem deleting that list'
