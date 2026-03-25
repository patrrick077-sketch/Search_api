from flask import Flask, request, jsonify
from duckduckgo_search import DDGS
from duckduckgo_search.exceptions import DuckDuckGoSearchException

app = Flask(__name__)

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q')
    max_results = request.args.get('max_results', default=5, type=int)

    if not query:
        return jsonify({"error": "Query parameter 'q' is required"}), 400

    try:
        # FIX: Define headers to mimic a real browser
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        }
        
        # FIX: Pass headers to DDGS
        with DDGS(headers=headers) as ddgs:
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
