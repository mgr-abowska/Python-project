from flask import Flask, render_template, session, redirect
import csv
import auth
import shelve

main = Flask(__name__)

main.config["SECRET_KEY"] = 'kwymgalskcnkgvbehdlknfdvhuh57v6655cy39jd'
main.register_blueprint(auth.auth)


@main.route('/')
def index():
    if not session.get('login'):
        return redirect('/login')

    return render_template('index.html', login=session['login'])


@main.route('/general')
def general():
    if not session.get('login'):
        return redirect('/login')

    with open('general_info.csv', newline='') as f:
        reader = csv.reader(f)
        g_data = list(reader)

    for i in g_data[1:]:
        for n in range(0, 4):
            i[n] = int(i[n])

    return render_template('general.html', g_data=str(g_data))


@main.route('/activity')
def activity():
    with open('data_one_day.csv', newline='') as f:
        reader = csv.reader(f)
        data = list(reader)
    print(data)

    [i.pop(3) for i in data]

    for i in data[1:]:
        for n in range(0, 3):
            i[n] = int(i[n])

    # print(data)
    return render_template('chart.html', data=str(data))


if __name__ == '__main__':
    main.run(debug=True)
