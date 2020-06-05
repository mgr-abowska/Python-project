from flask import Flask, render_template
import csv

main = Flask(__name__)

@main.route('/activity')
def activity():
    with open('data_one_hour_after.csv', newline='') as f:
        reader = csv.reader(f)
        data = list(reader)

    print(data)

    [i.pop(3) for i in data]

    for i in data[1:]:
        for n in range(0, 3):
            i[n] = int(i[n])

    #print(data)

    return render_template('chart.html', data = str(data[1:]))

if __name__ == '__main__':
    main.run(debug=True)