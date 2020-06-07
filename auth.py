from flask import Blueprint, request, render_template, redirect, session
import shelve

auth = Blueprint('auth', __name__, template_folder='templates')

db = shelve.open('base')


def if_exist(username):
    for i in db['users']:
        if username in i.values():
            return i
    return False


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    username = request.form['user']

    user = if_exist(username)
    print(request.form['user'])

    if user:
        session['login'] = username  # lepiej robić to po id
        return redirect('/')  # url for pozwala na dynamiczne określenie linków

    return render_template('login.html')


@auth.route('/logout', methods=['GET', 'POST'])
def logout():
    session['login'] = ''
    return redirect('/login')
