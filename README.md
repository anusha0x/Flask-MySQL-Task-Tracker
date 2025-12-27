# 🚀 Full-Stack Task Tracker API
This is a robust, full-stack Task Management application built using a Python RESTful API (Flask/MySQL) and a responsive frontend built with pure HTML, CSS, and Vanilla JavaScript.

The project demonstrates proficiency in database interaction, clean backend architecture, dynamic query handling, and seamless frontend integration.

# ✨ Features
The application provides a complete solution for managing tasks with the following capabilities:

-Full CRUD API: Supports all core REST operations: POST, GET, PUT, and DELETE.

-Partial Updates (PATCH): Allows for updating specific fields (e.g., description) without needing to send the entire task object.

-Dynamic Query Filtering & Sorting: The GET /tasks endpoint accepts URL parameters for filtering by status and sorting by fields like due_date or title.

-Modular Architecture: Uses Flask Blueprints to organize routes and a dedicated model layer for clean database logic.

-Full-Stack Integration: Frontend uses native JavaScript fetch for all asynchronous API communication, providing a fast and reactive user experience.

-CORS Enabled: Configured with Flask-CORS to handle cross-origin requests securely.

# 🛠️ Tech Stack
Category	Technology	Purpose
Backend-	Python, Flask	REST API Framework
Database-	MySQL	Persistent data storage
Frontend-	HTML5, CSS3, Vanilla JS	User Interface and API interaction
Dependencies-	mysql-connector-python, Flask-CORS	Database connectivity and security
# 🔌 API Endpoints
Method	Endpoint	Description	Query Parameters
POST	/tasks	Creates a new task.	None
GET	/tasks	Retrieves all tasks.	?status=pending, ?sort_by=due_date, ?sort_order=DESC
GET	/tasks/<id>	Retrieves a single task.	None
PUT	/tasks/<id>	Replaces the entire task (used for status toggle).	None
PATCH	/tasks/<id>	Updates specific fields of a task.	None
DELETE	/tasks/<id>	Deletes a task.	None


# ⚙️ Setup and Installation
Follow these steps to run the project locally:

Clone the Repository:

Bash
git clone [Your Repository URL]
cd task_tracker
Create and Activate Virtual Environment:

Bash
# Windows PowerShell
python -m venv venv
.\venv\Scripts\Activate.ps1

# macOS/Linux/Git Bash
python3 -m venv venv
source venv/bin/activate
Install Dependencies:

Bash
pip install -r requirements.txt
(You will need to create this file by running pip freeze > requirements.txt)

Database Setup:

Set up a MySQL database (e.g., named task_tracker).

Create a file named db_config.py (refer to the db_config_example.py for structure) and enter your credentials.

Run the Backend API:

Bash
python app.py
Access the Frontend: Open the frontend/index.html file in your web browser.
