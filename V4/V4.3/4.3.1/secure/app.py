from flask import Flask, render_template, request, jsonify
from graphql import parse
from graphql.language.visitor import Visitor, visit

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

MAX_QUERY_DEPTH = 3
MAX_QUERY_COST = 20

# Allowed operations (Query Allowlisting)
ALLOWED_QUERIES = [
    "IntrospectionQuery"
]

class DepthAndCostVisitor(Visitor):
    def __init__(self):
        self.max_depth = 0
        self.current_depth = 0
        self.cost = 0

    def enter_field(self, node, key, parent, path, ancestors):
        self.cost += 1  # Base cost for every field
        if node.selection_set:
            self.current_depth += 1
            if self.current_depth > self.max_depth:
                self.max_depth = self.current_depth

    def leave_field(self, node, key, parent, path, ancestors):
        if node.selection_set:
            self.current_depth -= 1

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/graphql', methods=['POST'])
def graphql_endpoint():
    data = request.get_json()
    query = data.get('query')
    if not query:
        return jsonify({"errors": [{"message": "Must provide query string."}]}), 400

    try:
        ast = parse(query)
    except Exception as e:
        return jsonify({"errors": [{"message": f"GraphQL Parse Error: {str(e)}"}]}), 400

    # AST Analysis for limits
    visitor = DepthAndCostVisitor()
    try:
        visit(ast, visitor)
    except Exception as e:
        return jsonify({"errors": [{"message": "Error analyzing query."}]}), 500

    if visitor.max_depth > MAX_QUERY_DEPTH:
        return jsonify({"errors": [{"message": f"Query exceeds maximum allowed depth of {MAX_QUERY_DEPTH}."}]}), 400

    if visitor.cost > MAX_QUERY_COST:
        return jsonify({"errors": [{"message": f"Query exceeds maximum allowed cost of {MAX_QUERY_COST}."}]}), 400

    # Execute
    result = schema.execute(query)
    
    response = {"data": result.data}
    if result.errors:
        response["errors"] = [str(err) for err in result.errors]
    
    response["extensions"] = {
        "depth": visitor.max_depth,
        "cost": visitor.cost
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
