from flask_app import app
from flask import render_template, redirect, session, request
from flask_app.models import painting, user
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/dashboard')
def dashboards():
    if "user_id" not in session:
        return redirect('/')
    data = {
        "id": session['user_id']
    }
    return render_template("painting_dashboard.html", painting = painting.Painting.get_all_user_paintings(), user = user.Person.user_get_id(data))

@app.route('/painting/add', methods = ['POST'])
def add_paintings():
    if 'user_id' not in session:
        return redirect('/')
    valid = painting.Painting.painting_validate(request.form)
    if valid:
        data = {
            'title': request.form['title'],
            'description': request.form['description'],
            'price': request.form['price'],
            'user_id': session['user_id']
        }
        paintings = painting.Painting.create_painting(data)
        return redirect('/dashboard')
    return redirect('/add/painting')

@app.route('/add/painting')
def add_new_painting():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': session['user_id']
    }
    return render_template("painting_add.html", user = user.Person.user_get_id(data))

@app.route('/painting/<int:painting_id>/edit')
def edit_painting(painting_id):
    data = {
        'id': painting_id
    }
    return render_template("painting_edit.html", painting = painting.Painting.get_a_painting(data))

@app.route('/paintings/<int:painting_id>/edit_in_db', methods = ['POST'])
def edit_your_painting(painting_id):
    if 'user_id' not in session:
        return redirect('/')
    if not painting.Painting.painting_validate(request.form):
        data = {
            'title': request.form['title'],
            'description': request.form['description'],
            'price': request.form['price'],
            'id': session['user_id']
        }
        paintings = painting.Painting.update_painting(data)
        return redirect('/dashboard')
    return redirect('/painting/<int:painting_id>/edit')

@app.route('/painting/<int:painting_id>/update', methods = ['POST'])
def update_painting(painting_id):
    painting.Painting.update_painting(request.form)
    return redirect('/dashboard')

@app.route('/show/<int:painting_id>/')
def show_painting_info(painting_id):
    data = {
        'id': painting_id
    }
    return render_template("painting_show.html", painting = painting.Painting.get_one(data))

@app.route('/painting/<int:id>/delete')
def delete(id):
    data = {
        "id": id
    }
    painting.Painting.delete_painting(data)
    return redirect('/dashboard')