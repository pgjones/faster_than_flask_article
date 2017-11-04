from quart import abort, Blueprint, current_app, jsonify, request

blueprint = Blueprint('reviews', __name__)


@blueprint.route('/reviews/', methods=['POST'])
async def add_review():
    data = await request.get_json()
    film_id = data['film_id']
    rating = int(data['rating'])
    async with current_app.pool.acquire() as connection:
        await connection.execute(
            """INSERT INTO review (film_id, rating)
                    VALUES ($1, $2)""",
            film_id, rating,
        )
    return jsonify({
        'film_id': film_id,
        'rating': rating,
    })
