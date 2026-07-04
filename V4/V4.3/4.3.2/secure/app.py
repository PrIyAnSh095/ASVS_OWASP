from flask import Flask, render_template, request, jsonify
import re

import graphene

class Profile(graphene.ObjectType):
    bio = graphene.String()

class Comment(graphene.ObjectType):
    text = graphene.String()

class Post(graphene.ObjectType):
    title = graphene.String()
    comments = graphene.List(Comment)

class User(graphene.ObjectType):
    id = graphene.ID()
    name = graphene.String()
    profile = graphene.Field(Profile)
    posts = graphene.List(Post)

class Query(graphene.ObjectType):
    users = graphene.List(User)

    def resolve_users(parent, info):
        return [
            User(id="1", name="Alice", profile=Profile(bio="Admin"), posts=[Post(title="Hello", comments=[Comment(text="Nice")])])
        ]

schema = graphene.Schema(query=Query)


app = Flask(__name__, template_folder='templates', static_folder='../static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/graphql', methods=['POST'])
def graphql_endpoint():
    data = request.get_json()
    query = data.get('query', '')
    
    # ASVS 4.3.2: Disable introspection queries
    if re.search(r'__(schema|type)', query):
        return jsonify({"errors": [{"message": "GraphQL introspection is not allowed in production."}]}), 400

    result = schema.execute(query)
    response = {"data": result.data}
    if result.errors:
        response["errors"] = [str(err) for err in result.errors]
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
