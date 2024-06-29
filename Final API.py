from flask import Flask, jsonify
from flask_cors import CORS
from flask_caching import Cache
from imdb import IMDb

app = Flask(__name__)
CORS(app)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})  # Configure caching

ia = IMDb()

@app.route('/media/<imdb_id>')
@cache.cached(timeout=3600)  # Cache response for 1 hour
def get_media_info(imdb_id):
    try:
        item = ia.get_movie(imdb_id[2:])

        if not item:
            return jsonify({'error': 'Movie not found'}), 404

        item_type = item.get('kind', 'N/A')
        title = item.get('title', 'N/A')
        poster_link = item.get('full-size cover url', 'N/A')
        description = item.get('plot', 'N/A')

        media_info = {
            'type': item_type,
            'title': title,
            'posterLink': poster_link,
            'description': description,
        }

        return jsonify(media_info)

    except Exception as e:
        app.logger.error('Error processing request: %s', str(e))
        return jsonify({'error': 'Internal Server Error'}), 500

if __name__ == '__main__':
    app.run(debug=True)
