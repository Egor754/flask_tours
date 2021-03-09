from random import sample

from flask import Flask, render_template, abort
from data import title, departures, tours, subtitle, description

app = Flask(__name__)


@app.route('/')
def render_index():
    random_tours = sample(list(tours.values()), 6)
    return render_template(
        'tours/index.html',
        departures=departures,
        random_tours=random_tours,
        title=title,
        subtitle=subtitle,
        description=description)


@app.route('/departures/<departure>/')
def render_departures(departure):
    tours_departure = {}
    for id,tour in tours.items():
        if tour['departure'] == departure:
            tours_departure[id] = tour
    return render_template('tours/departure.html', tours=tours_departure, departures=departures,title=title)


@app.route('/tours/<int:id>/')
def render_tour(id):
    if id not in tours:
        abort(404)
    tour = tours[id]
    return render_template('tours/tour.html')

@app.errorhandler(404)
def pageNotFound(error):
    return render_template('errors/404.html',departures=departures,title=title)


if __name__ == '__main__':
    app.run(debug=True)
