import os

base_dir = r"C:\Users\kakka\OneDrive\Desktop\ASVS-Labs\V4\V4.3\4.3.2"

def write_file(rel_path, content):
    full_path = os.path.join(base_dir, rel_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content.strip() + '\n')
    print(f"Written {rel_path}")

# --- HTML/CSS/JS ---
write_file(r"templates\layout.html", """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>ASVS 4.3.2 - GraphQL Introspection</title>
</head>
<body>
    <h1>ASVS 4.3.2: GraphQL Introspection</h1>
    {% block content %}{% endblock %}
</body>
</html>
""")

write_file(r"secure\templates\index.html", """
{% extends 'layout.html' %}
{% block content %}
    <h2>Secure GraphQL API</h2>
    <p>Introspection queries (__schema, __type) are disabled.</p>
    <textarea id="query" rows="10" cols="50">
query {
  __schema {
    types {
      name
    }
  }
}
    </textarea><br>
    <button id="executeBtn">Execute</button>
    <h3>Response:</h3>
    <div id="statusIndicator"></div>
    <pre id="responseViewer"></pre>

    <script>
        document.getElementById('executeBtn').addEventListener('click', async () => {
            const query = document.getElementById('query').value;
            const res = await fetch('/graphql', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ query })
            });
            const data = await res.json();
            document.getElementById('responseViewer').textContent = JSON.stringify(data, null, 2);
            document.getElementById('statusIndicator').textContent = (res.ok && !data.errors) ? "PASS" : "FAIL";
        });
    </script>
{% endblock %}
""")

write_file(r"vulnerable\templates\index.html", """
{% extends 'layout.html' %}
{% block content %}
    <h2>Vulnerable GraphQL API</h2>
    <p>Introspection queries are enabled.</p>
    <textarea id="query" rows="10" cols="50">
query {
  __schema {
    types {
      name
    }
  }
}
    </textarea><br>
    <button id="executeBtn">Execute</button>
    <h3>Response:</h3>
    <div id="statusIndicator"></div>
    <pre id="responseViewer"></pre>

    <script>
        document.getElementById('executeBtn').addEventListener('click', async () => {
            const query = document.getElementById('query').value;
            const res = await fetch('/graphql', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ query })
            });
            const data = await res.json();
            document.getElementById('responseViewer').textContent = JSON.stringify(data, null, 2);
            document.getElementById('statusIndicator').textContent = (res.ok && !data.errors) ? "PASS" : "FAIL";
        });
    </script>
{% endblock %}
""")

# Note: Keeping frontend minimal as requested. Empty CSS/JS to satisfy template structure if needed.
write_file(r"static\css\style.css", "")
write_file(r"static\js\app.js", "")

# --- GRAPHQL SCHEMA (SHARED) ---
schema_code = """
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
"""

# --- SECURE APP ---
write_file(r"secure\app.py", f"""
from flask import Flask, render_template, request, jsonify
import re
{schema_code}

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
        return jsonify({{"errors": [{{"message": "GraphQL introspection is not allowed in production."}}]}}), 400

    result = schema.execute(query)
    response = {{"data": result.data}}
    if result.errors:
        response["errors"] = [str(err) for err in result.errors]
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
""")

write_file(r"secure\requirements.txt", """
Flask==2.3.2
graphene==3.3.0
""")

write_file(r"secure\Dockerfile", """
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
COPY ../static /static
COPY ../templates /templates
CMD ["python", "app.py"]
""")

write_file(r"secure\docker-compose.yml", """
version: '3.8'
services:
  secure-graphql-432:
    build: .
    ports:
      - "5000:5000"
""")

write_file(r"secure\.env", "FLASK_ENV=development\n")
write_file(r"secure\README.md", """
# Secure Implementation - ASVS 4.3.2

This application disables GraphQL introspection.
It intercepts incoming queries and rejects those containing `__schema` or `__type` meta-fields.
This prevents attackers from discovering internal data models and available operations.
""")

# --- VULNERABLE APP ---
write_file(r"vulnerable\app.py", f"""
from flask import Flask, render_template, request, jsonify
{schema_code}

app = Flask(__name__, template_folder='templates', static_folder='../static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/graphql', methods=['POST'])
def graphql_endpoint():
    data = request.get_json()
    query = data.get('query', '')
    
    # VULNERABILITY: Introspection is left enabled.
    result = schema.execute(query)
    
    response = {{"data": result.data}}
    if result.errors:
        response["errors"] = [str(err) for err in result.errors]
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
""")

write_file(r"vulnerable\requirements.txt", """
Flask==2.3.2
graphene==3.3.0
""")

write_file(r"vulnerable\Dockerfile", """
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
COPY ../static /static
COPY ../templates /templates
CMD ["python", "app.py"]
""")

write_file(r"vulnerable\docker-compose.yml", """
version: '3.8'
services:
  vulnerable-graphql-432:
    build: .
    ports:
      - "5000:5000"
""")

write_file(r"vulnerable\.env", "FLASK_ENV=development\n")
write_file(r"vulnerable\README.md", """
# Vulnerable Implementation - ASVS 4.3.2

This application leaves GraphQL introspection enabled.
Attackers can send `__schema` queries to dump the entire API structure.
""")

# --- DOCS ---
write_file(r"docs\attack.md", """
# Attack Vectors for ASVS 4.3.2 (GraphQL Introspection)

GraphQL introspection is a built-in feature that allows clients to query the server for its schema. 
While useful for development (e.g., auto-completion in GraphQL Playground), it is a massive information disclosure vulnerability in production.

## Exploitation
An attacker can send a single query requesting the `__schema` field. 
The server will respond with a full JSON representation of every Type, Field, Query, Mutation, and Argument available.

## Impact
This exposes hidden administrative endpoints, internal data structures, and deprecated/vulnerable fields. 
Attackers use this mapped surface to craft precise targeted attacks.
""")

write_file(r"docs\burp.md", """
# Testing with Burp Suite

You can easily discover if a GraphQL endpoint has introspection enabled using Burp Suite.

## Discovery
1. Intercept any GraphQL POST request in Burp Suite Proxy.
2. Send the request to Repeater.
3. Replace the `query` field in the JSON body with a standard introspection payload (e.g., requesting `__schema { types { name } }`).
4. If the server responds with a 200 OK and a list of types, introspection is enabled (FAIL).
5. If the server responds with an error indicating introspection is disabled, the control is met (PASS).

*Burp Suite Extensions like InQL can automate this process.*
""")

write_file(r"docs\curl.md", """
# Testing with cURL

You can use cURL to quickly verify if introspection is enabled.

## Test Command
```bash
curl -X POST http://localhost:5000/graphql \\
-H "Content-Type: application/json" \\
-d '{"query": "query { __schema { types { name } } }"}'
```

## Secure Response (PASS)
The secure application will return a `400 Bad Request` with an error message: `"GraphQL introspection is not allowed in production."`

## Vulnerable Response (FAIL)
The vulnerable application will return a `200 OK` dumping the available schema types, such as `Query`, `User`, `Post`, and `Comment`.
""")

write_file(r"docs\expected.md", """
# Expected Behavior

## Secure Implementation
* Introspection queries containing `__schema` or `__type` are intercepted and rejected.
* A clear error message is returned.
* Standard application queries (e.g., fetching users) continue to function normally.

## Vulnerable Implementation
* Introspection queries are processed.
* The API returns its complete schema definition upon request, aiding attackers in reconnaissance.
""")

write_file(r"docs\notes.md", """
# Implementation Notes

* Most GraphQL frameworks (Apollo, Graphene, GraphQL-Java) enable introspection by default.
* Disabling it usually requires setting an explicit configuration flag (e.g., `introspection: false`) or adding a custom validation rule.
* In this lab, the secure application uses a simple string matching mechanism on the incoming query for educational clarity. In production, using the framework's native AST validation rules (`DisableIntrospectionRule`) is recommended.
""")

write_file(r"docs\solution.md", """
# Solution Guide

To satisfy ASVS 4.3.2, disable introspection in production.

1. Locate your GraphQL server configuration.
2. Check the framework documentation for the introspection setting.
3. Ensure it is conditionally tied to the environment variables (e.g., enabled if `NODE_ENV=development`, disabled if `NODE_ENV=production`).

Example for Apollo Server:
```javascript
const server = new ApolloServer({
  typeDefs,
  resolvers,
  introspection: process.env.NODE_ENV !== 'production'
});
```
""")

write_file(r"docs\theory.md", """
# Theoretical Background - ASVS 4.3.2

GraphQL is strongly typed and self-documenting. Introspection is the mechanism that powers this self-documentation.

## Security vs. Usability
In development, introspection is vital for IDE auto-completion and tools like GraphiQL. 
In production, it violates the principle of "Security through Obscurity" – though obscurity is not a primary defense, freely handing an attacker a complete map of your API greatly accelerates their reconnaissance phase.

ASVS 4.3.2 mandates disabling this feature in production to force attackers to guess or reverse-engineer the schema, significantly raising the barrier to entry for exploiting other vulnerabilities.
""")

# --- TESTS ---
write_file(r"tests\burp_requests.txt", """
POST /graphql HTTP/1.1
Host: localhost:5000
Content-Type: application/json

{"query": "query { __schema { types { name kind fields { name } } } }"}
""")

write_file(r"tests\burp_responses.txt", """
--- SECURE APPLICATION RESPONSE ---
HTTP/1.1 400 BAD REQUEST
Content-Type: application/json

{
  "errors": [
    {
      "message": "GraphQL introspection is not allowed in production."
    }
  ]
}

--- VULNERABLE APPLICATION RESPONSE ---
HTTP/1.1 200 OK
Content-Type: application/json

{
  "data": {
    "__schema": {
      "types": [
         // ... comprehensive schema dump ...
      ]
    }
  }
}
""")

write_file(r"tests\curl.txt", """
# Full Schema Introspection
curl -X POST http://localhost:5000/graphql \\
-H "Content-Type: application/json" \\
-d '{"query": "query { __schema { types { name fields { name type { name } } } } }"}'
""")

write_file(r"tests\payloads.txt", """
# Basic Introspection
query { __schema { types { name } } }

# Deep Introspection (Dumping Fields and Types)
query {
  __schema {
    types {
      name
      kind
      description
      fields {
        name
        type {
          name
          kind
          ofType {
            name
            kind
          }
        }
      }
    }
  }
}

# Type Introspection
query {
  __type(name: "User") {
    name
    fields {
      name
      type {
        name
      }
    }
  }
}
""")
