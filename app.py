from flask import Flask
from routes.task_routes import task_bp   # Import the Blueprint
from flask_cors import CORS

# Create Flask app instance
app = Flask(__name__)
CORS(app)

# Temporary in-memory storage for testing
tasks = [
    {
        "id": 1,
        "title": "Complete Flask Project",
        "description": "Finish all CRUD routes and test with Postman",
        "status": "pending",
        "created_at": "2025-10-16T10:20:00"
    }
]

# Register the Blueprint (to activate your routes)
app.register_blueprint(task_bp)

# Home route
@app.route('/', methods=['GET', 'POST'])
def home():
    return "✅ Student Task Tracker API is running successfully!"

# Run the app
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
 