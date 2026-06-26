from flask import Flask, render_template_string
import requests

app = Flask(__name__)

# A simple HTML string template so we don't have to create a separate templates folder
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Trending Anime Hub</title>
    <style>
        body { font-family: sans-serif; background: #121212; color: white; padding: 20px; text-align: center; }
        .grid { display: flex; flex-wrap: wrap; justify-content: center; gap: 20px; }
        .card { background: #1e1e1e; border-radius: 8px; padding: 15px; width: 200px; box-shadow: 0 4px 8px rgba(0,0,0,0.5); }
        img { width: 100%; border-radius: 4px; height: 280px; object-fit: cover; }
        h3 { font-size: 1rem; margin: 10px 0 5px 0; color: #ff4757; text-overflow: ellipsis; white-space: nowrap; overflow: hidden;}
        p { font-size: 0.85rem; color: #ccc; margin: 0; }
    </style>
</head>
<body>
    <h1>🔥 Current Top Trending Anime 🔥</h1>
    <p>This data is fetched live via Flask API Routing</p>
    <br>
    <div class="grid">
        {% for anime in anime_list %}
        <div class="card">
            <img src="{{ anime['images']['jpg']['image_url'] }}" alt="Cover">
            <h3>{{ anime['title'] }}</h3>
            <p>Score: ⭐ {{ anime['score'] }}</p>
            <p>Episodes: {{ anime['episodes'] }}</p>
        </div>
        {% endfor %}
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    # 1. Hit the open Jikan API endpoint for top anime
    api_url = "https://api.jikan.moe/v4/top/anime"
    
    try:
        response = requests.get(api_url)
        # 2. Extract JSON payload data
        data = response.json()
        # Jikan nests its results under a 'data' array key
        top_anime = data.get('data', [])[:10]  # Grab the top 10 items
    except Exception as e:
        top_anime = []
        print(f"Error fetching data: {e}")

    # 3. Route that dynamic data straight into the template layout
    return render_template_string(HTML_TEMPLATE, anime_list=top_anime)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
