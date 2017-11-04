from quart import abort, Blueprint, current_app, jsonify, request

blueprint = Blueprint('films', __name__)


@blueprint.route('/films/')
async def get_films():
    minimal_year = request.args.get('year.gt', 2000)
    films = {}
    async with current_app.pool.acquire() as connection:
        async with connection.transaction():
            async for film in connection.cursor(
                """SELECT film_id, release_year, title
                     FROM film
                    WHERE release_year > $1""",
                minimal_year,
            ):
                films[film['film_id']] = {
                    'release_year': film['release_year'],
                    'title': film['title'],
                }
    return jsonify(films)


@blueprint.route('/films/<int:id>/')
async def get_film(id):
    async with current_app.pool.acquire() as connection:
        async with connection.transaction():
            result = await connection.fetchrow(
                """SELECT film_id, release_year, title
                     FROM film
                    WHERE film_id = $1""",
                id,
            )
    if result is not None:
        return jsonify({
            'film_id': result['film_id'],
            'release_year': result['release_year'],
            'title': result['title'],
        })
    else:
        abort(404)
