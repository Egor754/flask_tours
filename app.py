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
    for pk, tour in tours.items():
        if tour['departure'] == departure:
            tours_departure[pk] = tour
    if not tours_departure:
        abort(404)
    departure_name = departures[departure].replace("Из", "из")
    prices = [price['price'] for price in tours_departure.values()]
    nights = [night['nights'] for night in tours_departure.values()]
    return render_template(
        'tours/departure.html',
        tours=tours_departure,
        departures=departures,
        departure_name=departure_name,
        title=title,
        pricemin=min(prices),
        pricemax=max(prices),
        nightmin=min(nights),
        nightmax=max(nights),
    )


@app.route('/tours/<int:id>/')
def render_tour(id):
    if id not in tours:
        abort(404)
    tour = tours[id]
    tour['departures'] = departures[tour['departure']]
    return render_template(
        'tours/tour.html',
        tour=tour,
        departures=departures,
        title=title
    )


# @app.context_processor
# def title_departures():
#     return title


@app.errorhandler(404)
def pageNotFound(error):
    return render_template('errors/404.html', departures=departures, title=title), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if __name__ == '__main__':
    app.run(debug=True)
