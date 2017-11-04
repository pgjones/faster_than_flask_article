from flask import abort, Blueprint, current_app, jsonify, request

blueprint = Blueprint('reviews', __name__)


@blueprint.route('/reviews/', methods=['POST'])
def add_review():
    data = request.get_json()
    film_id = data['film_id']
    rating = int(data['rating'])
    with current_app.pool.acquire() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """INSERT INTO review (film_id, rating)
                        VALUES (%s, %s)""",
                (film_id, rating),
            )
    return jsonify({
        'film_id': film_id,
        'rating': rating,
    })
