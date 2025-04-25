from flask import Flask, render_template, request, abort, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    done = db.Column(db.Boolean, default=False)

@app.route('/')
def index():
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    description = request.form['description']
    new_task = Task(description=description)
    db.session.add(new_task)
    db.session.commit()
    return render_template('_task.html', task=new_task)

@app.route('/toggle/<int:id>', methods=['POST'])
def toggle_task(id):
    task = Task.query.get(id)
    task.done = not task.done
    db.session.commit()
    return render_template('_task.html', task=task)

@app.route('/delete/<int:id>', methods=['POST'])
def delete_task(id):
    task = Task.query.get(id)
    if task:
        db.session.delete(task)
        db.session.commit()
        return (redirect(url_for('index')))

# Criação do banco ao iniciar
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
