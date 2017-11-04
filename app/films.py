from flask import abort, Blueprint, current_app, jsonify, request

blueprint = Blueprint('films', __name__)


@blueprint.route('/films/')
def get_films():
    minimal_year = request.args.get('year.gt', 2000)
    films = {}
    with current_app.pool.acquire() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """SELECT film_id, release_year, title
                     FROM film
                    WHERE release_year > %s""",
                (minimal_year,),
            )
            for film in cursor:
                films[film['film_id']] = {
                    'release_year': film['release_year'],
                    'title': film['title'],
                }
    return jsonify(films)


@blueprint.route('/films/<int:id>/')
def get_film(id):
    with current_app.pool.acquire() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """SELECT film_id, release_year, title
                     FROM film
                    WHERE film_id = %s""",
                (id,),
            )
            result = cursor.fetchone()
    if result is not None:
        return jsonify({
            'film_id': result['film_id'],
            'release_year': result['release_year'],
            'title': result['title'],
        })
    else:
        abort(404)
