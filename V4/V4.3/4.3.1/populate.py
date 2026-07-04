import os

base_dir = r"C:\Users\kakka\OneDrive\Desktop\ASVS-Labs\V4\V4.3\4.3.1"

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
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ASVS 4.3.1 - GraphQL Query Limits</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>
<body>
    <header>
        <h1>ASVS 4.3.1 Lab: GraphQL Denial of Service</h1>
    </header>
    <main>
        {% block content %}{% endblock %}
    </main>
    <script src="{{ url_for('static', filename='js/app.js') }}"></script>
</body>
</html>
""")

write_file(r"secure\templates\index.html", """
{% extends 'layout.html' %}
{% block content %}
<div class="container">
    <h2>Secure GraphQL API</h2>
    <p>This implementation enforces query depth limits, cost analysis, and limits on returned objects to prevent DoS attacks.</p>
    
    <div class="graphql-playground">
        <div class="editor-section">
            <label for="query">GraphQL Query:</label>
            <textarea id="query" rows="15">
{
  users {
    name
    posts {
      title
      comments {
        text
        author {
          name
        }
      }
    }
  }
}
            </textarea>
            <button id="executeBtn">Execute Query</button>
        </div>
        <div class="result-section">
            <h3>Response:</h3>
            <div id="indicators">
                <span id="statusIndicator">Status: N/A</span> | 
                <span id="depthIndicator">Depth: N/A</span> |
                <span id="costIndicator">Cost: N/A</span>
            </div>
            <pre id="responseViewer">{}</pre>
        </div>
    </div>
</div>
{% endblock %}
""")

write_file(r"vulnerable\templates\index.html", """
{% extends 'layout.html' %}
{% block content %}
<div class="container">
    <h2>Vulnerable GraphQL API</h2>
    <p>This implementation does NOT enforce any limits. Expensive, deeply nested queries will be fully executed, leading to resource exhaustion.</p>
    
    <div class="graphql-playground">
        <div class="editor-section">
            <label for="query">GraphQL Query:</label>
            <textarea id="query" rows="15">
{
  users {
    friends {
      friends {
        friends {
          friends {
            name
          }
        }
      }
    }
  }
}
            </textarea>
            <button id="executeBtn">Execute Query</button>
        </div>
        <div class="result-section">
            <h3>Response:</h3>
            <div id="indicators">
                <span id="statusIndicator">Status: N/A</span>
            </div>
            <pre id="responseViewer">{}</pre>
        </div>
    </div>
</div>
{% endblock %}
""")

write_file(r"static\css\style.css", """
body {
    font-family: Arial, sans-serif;
    margin: 0;
    padding: 0;
    background-color: #f4f4f9;
}
header {
    background-color: #333;
    color: #fff;
    padding: 1rem;
    text-align: center;
}
.container {
    max-width: 900px;
    margin: 2rem auto;
    background: #fff;
    padding: 2rem;
    border-radius: 8px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}
.graphql-playground {
    display: flex;
    gap: 2rem;
    margin-top: 1rem;
}
.editor-section, .result-section {
    flex: 1;
}
textarea {
    width: 100%;
    padding: 0.5rem;
    font-family: monospace;
    font-size: 14px;
    border: 1px solid #ccc;
    border-radius: 4px;
    resize: vertical;
}
button {
    background-color: #007bff;
    color: white;
    padding: 0.75rem 1.5rem;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    margin-top: 1rem;
    width: 100%;
    font-weight: bold;
}
button:hover {
    background-color: #0056b3;
}
pre {
    background: #272822;
    color: #f8f8f2;
    padding: 1rem;
    border-radius: 4px;
    overflow-x: auto;
    min-height: 200px;
}
#indicators {
    margin-bottom: 0.5rem;
    font-size: 14px;
    font-weight: bold;
}
.pass { color: green; }
.fail { color: red; }
""")

write_file(r"static\js\app.js", """
document.addEventListener('DOMContentLoaded', () => {
    const executeBtn = document.getElementById('executeBtn');
    if (executeBtn) {
        executeBtn.addEventListener('click', async () => {
            const query = document.getElementById('query').value;
            const responseViewer = document.getElementById('responseViewer');
            const statusIndicator = document.getElementById('statusIndicator');
            const depthIndicator = document.getElementById('depthIndicator');
            const costIndicator = document.getElementById('costIndicator');
            
            responseViewer.textContent = 'Executing...';
            
            try {
                const res = await fetch('/graphql', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ query })
                });
                
                const data = await res.json();
                responseViewer.textContent = JSON.stringify(data, null, 2);
                
                if (res.ok && !data.errors) {
                    statusIndicator.textContent = 'Status: PASS';
                    statusIndicator.className = 'pass';
                } else {
                    statusIndicator.textContent = 'Status: FAIL';
                    statusIndicator.className = 'fail';
                }

                if (data.extensions) {
                    if (depthIndicator) depthIndicator.textContent = 'Depth: ' + (data.extensions.depth || 'N/A');
                    if (costIndicator) costIndicator.textContent = 'Cost: ' + (data.extensions.cost || 'N/A');
                }

            } catch (err) {
                responseViewer.textContent = 'Network Error: ' + err.message;
                statusIndicator.textContent = 'Status: ERROR';
                statusIndicator.className = 'fail';
            }
        });
    }
});
""")


# --- GRAPHQL SCHEMA (SHARED LOGIC, WE WILL COPY THIS INTO BOTH) ---
schema_code = """
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
"""

# --- SECURE APP ---
write_file(r"secure\app.py", f"""
from flask import Flask, render_template, request, jsonify
from graphql import parse
from graphql.language.visitor import Visitor, visit
{schema_code}

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
        return jsonify({{"errors": [{{"message": "Must provide query string."}}]}}), 400

    try:
        ast = parse(query)
    except Exception as e:
        return jsonify({{"errors": [{{"message": f"GraphQL Parse Error: {{str(e)}}"}}]}}), 400

    # AST Analysis for limits
    visitor = DepthAndCostVisitor()
    try:
        visit(ast, visitor)
    except Exception as e:
        return jsonify({{"errors": [{{"message": "Error analyzing query."}}]}}), 500

    if visitor.max_depth > MAX_QUERY_DEPTH:
        return jsonify({{"errors": [{{"message": f"Query exceeds maximum allowed depth of {{MAX_QUERY_DEPTH}}."}}]}}), 400

    if visitor.cost > MAX_QUERY_COST:
        return jsonify({{"errors": [{{"message": f"Query exceeds maximum allowed cost of {{MAX_QUERY_COST}}."}}]}}), 400

    # Execute
    result = schema.execute(query)
    
    response = {{"data": result.data}}
    if result.errors:
        response["errors"] = [str(err) for err in result.errors]
    
    response["extensions"] = {{
        "depth": visitor.max_depth,
        "cost": visitor.cost
    }}

    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
""")

write_file(r"secure\requirements.txt", """
Flask==2.3.2
graphene==3.3.0
graphql-core==3.2.3
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
  secure-graphql:
    build: .
    ports:
      - "5000:5000"
""")

write_file(r"secure\.env", """
FLASK_APP=app.py
FLASK_ENV=development
""")

write_file(r"secure\README.md", """
# Secure Implementation - ASVS 4.3.1

This application demonstrates a secure GraphQL API that enforces limits on queries to prevent Denial of Service (DoS).

## Security Controls Implemented
* **Depth Limiting:** The API parses the GraphQL AST and rejects any query with a nesting depth greater than 3. This prevents cyclical relationship exhaustion.
* **Cost Analysis:** The API assigns a basic cost to each requested field. If the total cost exceeds 20, the query is rejected.
* **Meaningful Errors:** Instead of executing and crashing, the server returns a 400 Bad Request with a clear message indicating which limit was breached.
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
    query = data.get('query')
    if not query:
        return jsonify({{"errors": [{{"message": "Must provide query string."}}]}}), 400

    # VULNERABILITY: Directly executing without analyzing depth, cost, or limits.
    # An attacker can send extremely deep or expensive queries.
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
  vulnerable-graphql:
    build: .
    ports:
      - "5000:5000"
""")

write_file(r"vulnerable\.env", """
FLASK_APP=app.py
FLASK_ENV=development
""")

write_file(r"vulnerable\README.md", """
# Vulnerable Implementation - ASVS 4.3.1

This application provides a GraphQL API without any protection against expensive or deeply nested queries.

## The Vulnerability
GraphQL allows clients to specify exactly what data they want. Because the data model often contains recursive or cyclical relationships (e.g., `User` -> `friends` -> `User` -> `friends`), an attacker can request a massive amount of data in a single request. 

Since this server performs no Depth Limiting, Cost Analysis, or Allowlisting, it will attempt to fulfill arbitrarily large queries, leading to CPU and memory exhaustion (Denial of Service).
""")


# --- DOCS ---
write_file(r"docs\attack.md", """
# Attack Vectors for ASVS 4.3.1 (GraphQL DoS)

GraphQL shifts the power of query definition from the server to the client. This flexibility introduces a significant attack vector if queries are not constrained.

## Recursive Queries (Depth Exhaustion)
If the schema contains cyclical relationships (e.g., a `User` has `friends`, who are also `Users`), an attacker can craft a query that nests endlessly:
```graphql
query {
  users {
    friends {
      friends {
        friends {
          name
        }
      }
    }
  }
}
```
This forces the backend to resolve the database relationships recursively, exponentially increasing the workload and memory allocation until the server crashes.

## Resource Intensive Queries (Cost Exhaustion)
Even without deep recursion, requesting thousands of nodes and fields simultaneously (e.g., requesting 10,000 comments, their authors, and the author's profiles in a single shot) forces the server to do massive database joins and JSON serialization, locking up CPU threads and denying service to legitimate users.
""")

write_file(r"docs\burp.md", """
# Testing with Burp Suite

You can use Burp Suite to test a GraphQL endpoint for DoS vulnerabilities by sending deeply nested or highly complex payloads.

## Steps

1. **Intercept a GraphQL Request:** Find any request hitting `/graphql`. It will typically be a POST request with a JSON body containing `{"query": "..."}`.
2. **Send to Repeater:** Right-click and send the request to the Repeater tab.
3. **Modify the Query:**
   * Craft a deeply nested query exploiting cyclical relationships in the schema (e.g., user -> friends -> friends...).
   * Alternatively, request an excessive number of fields by using GraphQL aliases to request the same expensive field 100 times.
4. **Execute and Observe:**
   * **Secure Implementation:** Should immediately respond with a `400 Bad Request` or a GraphQL error object stating "Query exceeds maximum depth" or "Query exceeds maximum cost". The response time should be nearly instantaneous.
   * **Vulnerable Implementation:** The server will take a noticeably long time to respond, potentially timing out, crashing, or returning an enormous JSON payload. Sending multiple such requests concurrently will likely crash the service entirely.
""")

write_file(r"docs\curl.md", """
# Testing with cURL

You can use cURL to send malicious GraphQL payloads from the command line to test for depth limits.

## Secure App Test
```bash
curl -X POST http://localhost:5000/graphql \\
-H "Content-Type: application/json" \\
-d '{"query": "{ users { friends { friends { friends { friends { name } } } } } }"}'
```
**Expected Result:** The server parses the AST, calculates the depth, and immediately returns an error indicating the maximum depth (e.g., 3) was exceeded.

## Vulnerable App Test
```bash
curl -X POST http://localhost:5000/graphql \\
-H "Content-Type: application/json" \\
-d '{"query": "{ users { friends { friends { friends { friends { friends { friends { friends { name } } } } } } } } }"}'
```
**Expected Result:** The server executes the entire query, returning a massive, deeply nested JSON response, consuming significant backend resources.
""")

write_file(r"docs\expected.md", """
# Expected Behavior

## Secure Implementation
* **AST Parsing Validation:** The server parses the incoming GraphQL query string into an Abstract Syntax Tree (AST) before executing it.
* **Depth & Cost Calculation:** The server traverses the AST to calculate the query's depth and assigned computational cost.
* **Enforcement:** If either the depth or cost limit is exceeded, the execution is halted immediately. A clear GraphQL error is returned to the user.
* **Resource Preservation:** The server remains available and responsive because malicious queries are dropped before interacting with the data layer.

## Vulnerable Implementation
* **Unrestricted Execution:** The server blindly executes any valid GraphQL query it receives.
* **Resource Exhaustion:** Deeply nested queries cause explosive data retrieval and serialization, dragging down CPU and memory.
* **Denial of Service:** Concurrently sending a few heavy queries will lock up the application's request threads, causing timeouts for other legitimate users.
""")

write_file(r"docs\notes.md", """
# Implementation Notes

* In Python, `graphql-core` provides utilities (`parse` and `Visitor`) to analyze the AST of a query before handing it to the execution engine.
* **Query Cost:** In a production scenario, different fields should have different costs. Fetching a scalar string like `name` might cost 1, whereas fetching a computed relationship like `friends` might cost 10. The secure app demonstrates a simplified uniform cost model.
* **Persisted Queries / Allowlisting:** Another highly effective defense (especially for mobile/frontend apps with fixed queries) is to hash the queries on the frontend, register them on the backend, and only allow execution of known hashes. This completely neutralizes arbitrary complex queries from attackers.
""")

write_file(r"docs\solution.md", """
# Solution Guide

To secure a GraphQL API against expensive queries (ASVS 4.3.1), implement one or more of the following strategies:

1. **Depth Limiting:**
   * Use an AST parser or a middleware (like `graphql-depth-limit` in Node.js, or a custom AST visitor in Python) to calculate the maximum nesting depth of the query. Reject queries exceeding a reasonable threshold (e.g., 5).
2. **Query Cost Analysis:**
   * Assign point values to fields based on their computational expense. Sum the points before execution. Reject if the total exceeds a maximum allowed budget.
3. **Amount Limiting (Pagination limits):**
   * Enforce strict maximums on arguments like `first` or `limit` (e.g., `users(first: 100)`). Never allow unbounded lists.
4. **Query Allowlisting (Persisted Queries):**
   * If your API only serves your own frontends, pre-compile all legitimate queries and store their hashes on the server. The server should reject any query structure it hasn't seen before.
""")

write_file(r"docs\theory.md", """
# Theoretical Background - ASVS 4.3.1

GraphQL represents a paradigm shift from REST. Instead of the server dictating the shape and size of the response, the client requests exactly what it needs. While powerful for frontend developers, it is inherently dangerous for server stability.

## The N+1 Problem and Exponential Complexity
If an API exposes cyclical graphs, a simple 10-line query can trigger thousands of database calls. For example, requesting authors, their posts, those posts' comments, and the commenters' profiles.

Without defenses, GraphQL APIs are trivially susceptible to Application-Layer Denial of Service (DoS) attacks. Attackers don't need botnets; a single script sending complex queries can exhaust a database connection pool or OOM (Out of Memory) the application server.

ASVS 4.3.1 mandates that controls like Depth Limiting, Cost Analysis, or Allowlisting must be in place to cap the computational complexity an individual query can request.
""")


# --- TESTS ---
write_file(r"tests\burp_requests.txt", """
POST /graphql HTTP/1.1
Host: localhost:5000
Content-Type: application/json

{"query": "query { users { friends { friends { friends { friends { friends { name } } } } } } }"}
""")

write_file(r"tests\burp_responses.txt", """
--- SECURE APPLICATION RESPONSE ---
HTTP/1.1 400 BAD REQUEST
Content-Type: application/json

{
  "errors": [
    {
      "message": "Query exceeds maximum allowed depth of 3."
    }
  ]
}

--- VULNERABLE APPLICATION RESPONSE ---
HTTP/1.1 200 OK
Content-Type: application/json

{
  "data": {
    "users": [
      {
        "friends": [
           // ... massive nested JSON payload continuing for thousands of lines
        ]
      }
    ]
  }
}
""")

write_file(r"tests\curl.txt", """
# Secure App - Legitimate Query
curl -X POST http://localhost:5000/graphql \\
-H "Content-Type: application/json" \\
-d '{"query": "{ users { name } }"}'

# Secure App - Exceeding Depth Limit
curl -X POST http://localhost:5000/graphql \\
-H "Content-Type: application/json" \\
-d '{"query": "{ users { friends { friends { friends { name } } } } }"}'

# Vulnerable App - Extreme Depth Payload
curl -X POST http://localhost:5001/graphql \\
-H "Content-Type: application/json" \\
-d '{"query": "{ users { friends { friends { friends { friends { friends { name } } } } } } }"}'
""")

write_file(r"tests\payloads.txt", """
# Payload 1: Depth Exhaustion (Cyclical)
query {
  users {
    friends {
      friends {
        friends {
          friends {
            friends {
              friends {
                name
              }
            }
          }
        }
      }
    }
  }
}

# Payload 2: Cost Exhaustion (Alias Overloading)
query {
  a: users { name }
  b: users { name }
  c: users { name }
  d: users { name }
  e: users { name }
  f: users { name }
  g: users { name }
  h: users { name }
  i: users { name }
  j: users { name }
  # ... repeat 100 times to inflate the cost without increasing depth
}
""")
