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

    print(g_data)

    return render_template('general.html', g_data=str(g_data))


@main.route('/activity')
def activity():
    with open('data_one_day.csv', newline='') as f:
        reader = csv.reader(f)
        data = list(reader)

    data = []
    db = shelve.open('db')
    if db.items == []:
        return
        #Brak danych
    for x in db.items():
        date,username = x[0].split('||')
        if usermane.rstrip().lstrip() == session.get('login'):
            data.append([date,x[1]['followers_count'],x[1]['following_count'],x[1]['post_count'],
                        x[1]['average_post_likes'],x[1]['comments_analysis']])
    data.append(['2020-05-12',1,2,3,4,5])
    data.append(['2020-05-12',3,4,6,7,8])

    print(data)

    return render_template('chart.html', data=str(data))


# @main.route('/bot')
# def bot():


# @main.route('/rating')
# def rating():

if __name__ == '__main__':
    main.run(debug=True)
