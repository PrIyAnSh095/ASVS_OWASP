from flask import Flask, render_template, request, jsonify

import graphene
import json

class Profile(graphene.ObjectType):
    bio = graphene.String()
    website = graphene.String()

class Comment(graphene.ObjectType):
    text = graphene.String()
    author = graphene.Field(lambda: User)

class Post(graphene.ObjectType):
    title = graphene.String()
    content = graphene.String()
    comments = graphene.List(Comment)
    author = graphene.Field(lambda: User)

class User(graphene.ObjectType):
    id = graphene.ID()
    name = graphene.String()
    profile = graphene.Field(Profile)
    posts = graphene.List(Post)
    friends = graphene.List(lambda: User)

    def resolve_friends(parent, info):
        # Mock resolving friends (to allow infinite looping essentially)
        return MOCK_USERS

    def resolve_posts(parent, info):
        return [Post(title=f"Post by {parent.name}", content="Some content")]

# Mock Data
MOCK_USERS = [
    User(id="1", name="Alice", profile=Profile(bio="Hacker", website="alice.local")),
    User(id="2", name="Bob", profile=Profile(bio="Developer", website="bob.local"))
]

class Query(graphene.ObjectType):
    user = graphene.Field(User, id=graphene.ID(required=True))
    users = graphene.List(User)

    def resolve_user(parent, info, id):
        for u in MOCK_USERS:
            if u.id == id: return u
        return None

    def resolve_users(parent, info):
        return MOCK_USERS

schema = graphene.Schema(query=Query)


app = Flask(__name__, template_folder='templates', static_folder='../static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/graphql', methods=['POST'])
def graphql_endpoint():
    data = request.get_json()
    query = data.get('query')
    if not query:
        return jsonify({"errors": [{"message": "Must provide query string."}]}), 400

    # VULNERABILITY: Directly executing without analyzing depth, cost, or limits.
    # An attacker can send extremely deep or expensive queries.
    result = schema.execute(query)
    
    response = {"data": result.data}
    if result.errors:
        response["errors"] = [str(err) for err in result.errors]

    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
