from flask import Flask, request, jsonify
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

app = Flask(__name__)

# Your Configuration
GOOGLE_API_KEY = "AIzaSyA6Emqb7UDV6YpPF73lpSWisp2S3TozIoM" 
SEARCH_ENGINE_ID = "d500bbe9087814855"

@app.route('/search', methods=['GET'])
def search():
    # Get the query from the URL parameters (e.g., /search?q=hello)
    query = request.args.get('q')
    num_results = request.args.get('num', default=5, type=int)

    if not query:
        return jsonify({"error": "Please provide a query parameter 'q'"}), 400

    try:
        # 1. Initialize the Custom Search API service
        service = build("customsearch", "v1", developerKey=GOOGLE_API_KEY)

        # 2. Execute the search request
        # q: query string
        # cx: custom search engine ID
        # num: number of results (max 10 per request for this API)
        result = service.cse().list(
            q=query, 
            cx=SEARCH_ENGINE_ID, 
            num=num_results
        ).execute()

        # 3. Extract relevant data from the response
        search_results = []
        if 'items' in result:
            for item in result['items']:
                search_results.append({
                    "title": item.get('title'),
                    "link": item.get('link'),
                    "snippet": item.get('snippet'),
                    "display_link": item.get('displayLink')
                })

        return jsonify({
            "success": True,
            "query": query,
            "count": len(search_results),
            "results": search_results
        })

    except HttpError as e:
        # Handle Google API specific errors (like quota exceeded)
        error_details = e.content.decode('utf-8')
        return jsonify({
            "error": "Google API Error", 
            "details": error_details
        }), e.resp.status
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
