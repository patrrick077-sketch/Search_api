from flask import Flask, request, jsonify
from duckduckgo_search import DDGS
from duckduckgo_search.exceptions import DuckDuckGoSearchException

app = Flask(__name__)

@app.route('/search', methods=['GET'])
def search():
    """
    General Search Endpoint
    Query Params:
    - q: The search query (required)
    - max_results: Number of results to return (optional, default 5)
    """
    query = request.args.get('q')
    max_results = request.args.get('max_results', default=5, type=int)

    if not query:
        return jsonify({"error": "Query parameter 'q' is required"}), 400

    try:
        # DDGS is a context manager that handles the session
        with DDGS() as ddgs:
            # text() returns a generator, so we convert it to a list
            results = list(ddgs.text(query, max_results=max_results))
            
            return jsonify({
                "query": query,
                "count": len(results),
                "results": results
            })

    except DuckDuckGoSearchException as e:
        return jsonify({"error": f"Search engine error: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500


@app.route('/search/images', methods=['GET'])
def search_images():
    """
    Image Search Endpoint
    Query Params:
    - q: The search query (required)
    - max_results: Number of results to return (optional, default 5)
    """
    query = request.args.get('q')
    max_results = request.args.get('max_results', default=5, type=int)

    if not query:
        return jsonify({"error": "Query parameter 'q' is required"}), 400

    try:
        with DDGS() as ddgs:
            results = list(ddgs.images(query, max_results=max_results))
            
            return jsonify({
                "query": query,
                "count": len(results),
                "results": results
            })

    except DuckDuckGoSearchException as e:
        return jsonify({"error": f"Search engine error: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    # Debug=True allows auto-reloading during development
    app.run(debug=True, port=5000)
