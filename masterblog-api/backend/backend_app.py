from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


@app.route('/api/posts', methods=['GET'])
def get_posts():

    results = POSTS.copy()

    sort_field = request.args.get('sort')
    direction = request.args.get('direction', 'asc')

    reverse = False
    if direction == 'desc':
        reverse = True
    elif direction != 'asc':
        return jsonify({"error": "Invalid direction"}), 400

    results.sort(key=lambda post: post[sort_field].lower(), reverse=reverse)

    return jsonify(results), 200


@app.route('/api/posts', methods=['POST'])
def add_post():

    data = request.get_json()

    if not data or 'title' not in data or 'content' not in data:
        return jsonify({"error": "Missing 'title' or 'content'"}), 400

    new_id = max(post['id'] for post in POSTS) + 1 if POSTS else 1

    new_post = {"id": new_id,
                "title": data['title'],
                "content": data['content']}

    POSTS.append(new_post)

    return jsonify(new_post), 201

@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):

    post_to_delete = next((post for post in POSTS if post['id'] == post_id), None)

    if post_to_delete:
        POSTS.remove(post_to_delete)
        return jsonify({"message": f"Post with id {post_id} deleted."})
    else:
        return  jsonify({"message": f"Post with id {post_id} not found."}), 404

@app.route('/api/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):

    post_to_update = next((post for post in POSTS if post['id'] == post_id), None)
    if not post_to_update:
        return jsonify({"message": "Post not found."}), 404

    data = request.get_json()
    if 'title' in data:
        post_to_update['title'] = data['title']
    if 'content' in data:
        post_to_update['content'] = data['content']

    return jsonify(post_to_update), 200

@app.route('/api/posts/search', methods=['GET'])
def search_posts():

    title_query = request.args.get('title')
    content_query = request.args.get('content')

    results = POSTS

    if title_query:
        title_query = title_query.lower()
        results = [post for post in POSTS if title_query in post['title'].lower()]

    if content_query:
        content_query = content_query.lower()
        results = [post for post in POSTS if content_query in post['content'].lower()]

    return jsonify(results), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5003, debug=True)
