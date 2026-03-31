# Task Manager

A simple and intuitive web-based task management application built with Flask backend and vanilla JavaScript frontend. Organize your daily activities, create tasks and boost your productivity with an easy-to-use interface.

## Features

- **User Authentication**: Secure user registration and login functionality
- **Task Management**: Create, read, update, and delete tasks
- **Task Status Tracking**: Mark tasks as pending or completed
- **User Profile**: View and manage user account information
- **Task Statistics**: See statistics about your tasks (total, completed, pending)
- **Responsive Design**: Modern, clean UI with light green theme
- **Session Management**: localStorage-based session persistence

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.7+** - [Download Python](https://www.python.org/downloads/)
- **MySQL Server** - [Download MySQL](https://dev.mysql.com/downloads/mysql/)
- **Node.js & npm** (optional, for frontend development tools)
- **Git** - [Download Git](https://git-scm.com/)

## Project Structure

```
TaskManager/
├── backend/
│   ├── app.py                 # Main Flask application
│   ├── db.py                  # Database connection helper
│   ├── __pycache__/           # Python cache
│   ├── templates/             # Flask templates (if needed)
│   └── requirements.txt       # Python dependencies
├── frontend/
│   ├── index.html             # Landing page (register/login)
│   ├── register.html          # User registration page
│   ├── login.html             # User login page
│   ├── home.html              # Dashboard (authenticated users)
│   ├── tasks.html             # Task list page
│   ├── add-task.html          # Add new task page
│   ├── profile.html           # User profile page
│   ├── script.js              # Main JavaScript functionality
│   └── style.css              # Application styling
└── README.md                  # This file
```

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd TaskManager
```

### 2. Database Setup

#### Step 1: Create MySQL Database

Open MySQL command line and run the following commands:

```sql
-- Create the database
CREATE DATABASE task_manager;

-- Use the database
USE task_manager;

-- Create users table
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create tasks table
CREATE TABLE tasks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    status VARCHAR(20) DEFAULT 'pending',
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Create indexes for better query performance
CREATE INDEX idx_user_email ON users(email);
CREATE INDEX idx_task_user_id ON tasks(user_id);
CREATE INDEX idx_task_status ON tasks(status);
```

#### Step 2: Verify Database Connection

Update database credentials in `backend/db.py` if necessary:

```python
db_config = {
    'host': 'localhost',
    'user': 'root',              # Your MySQL username
    'password': 'your_password', # Your MySQL password
    'database': 'task_manager'
}
```

### 3. Backend Setup

#### Step 1: Navigate to Backend Directory

```bash
cd backend
```

#### Step 2: Create Virtual Environment (Recommended)

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

#### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

**If requirements.txt doesn't exist, install manually:**

```bash
pip install flask
pip install flask-cors
pip install mysql-connector-python
```

#### Step 4: Verify Backend Setup

All backend files should be present:
- `app.py` - Main Flask application with routes and API endpoints
- `db.py` - Database connection configuration

### 4. Frontend Setup

The frontend doesn't require installation as it uses vanilla JavaScript. Just ensure all HTML, CSS, and JS files are in the `frontend/` directory.

## How to Run the Application

### Running the Backend

1. Navigate to the backend directory:
```bash
cd backend
```

2. Activate virtual environment (if created):
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`

3. Run the Flask application:
```bash
python app.py
```

**Expected output:**
```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
```

The backend will start on `http://127.0.0.1:5000`

### Running the Frontend

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Open `index.html` in your browser:
   - Simply double-click `index.html`, OR
   - Use a local server (recommended for better compatibility):
   
   **Using Python's built-in server:**
   ```bash
   python -m http.server 8000
   ```
   Then visit: `http://127.0.0.1:8000`

   **Using Node.js http-server:**
   ```bash
   npx http-server
   ```

3. The application will open to the landing page at `http://127.0.0.1:8000`

## API Endpoints

### Authentication Routes

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/register` | User registration |
| POST | `/api/login` | User login |
| GET | `/user/<id>` | Get user profile information |

### Task Routes

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/tasks` | Get all tasks |
| POST | `/api/tasks` | Create a new task |
| PUT | `/api/tasks/<id>` | Update task status |
| DELETE | `/api/tasks/<id>` | Delete a task |

### Page Routes

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Landing page |
| GET | `/register` | Registration page |
| GET | `/login` | Login page |
| GET | `/home` | Home dashboard |
| GET | `/tasks` | Task list page |
| GET | `/add-task` | Add task page |
| GET | `/profile` | User profile page |

## Database Schema

### Users Table
```sql
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Tasks Table
```sql
CREATE TABLE tasks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    status VARCHAR(20) DEFAULT 'pending',
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

**Task Status Values:**
- `pending` - Task is not yet completed
- `completed` - Task has been marked as complete

## User Journey

1. **Landing Page** (`/`) - User sees welcome page with register/login options
2. **Registration** (`/register`) - New users create account with name, email, password
3. **Login** (`/login`) - Users authenticate with email and password
4. **Home Dashboard** (`/home`) - Authenticated users see welcome screen and quick actions
5. **Tasks** (`/tasks`) - View all tasks with status badges and action buttons
6. **Add Task** (`/add-task`) - Create new task with title and description
7. **Profile** (`/profile`) - View user profile and task statistics
8. **Logout** - Clear session and return to landing page

## Assumptions & Trade-offs

### Assumptions Made

1. **Password Security**: Currently, passwords are stored without hashing. In production, use bcrypt or similar libraries for password hashing.
2. **Single User Context**: Each browser session maintains one logged-in user via localStorage.
3. **Local Development**: Application assumes MySQL server is running on `localhost:3306`.
4. **Browser Support**: Modern browsers with ES6 JavaScript support (Chrome, Firefox, Safari, Edge).
5. **Synchronous Operations**: No complex async patterns; straightforward promise-based API calls.

### Trade-offs Made

1. **No Authentication Token**: Using localStorage for session management instead of JWT tokens for simplicity.
2. **No Password Encryption**: Passwords stored as plain text in database (use bcrypt in production).
3. **Vanilla JavaScript**: No frontend framework for minimal dependencies and learning curve.
4. **No Pagination**: All tasks load at once (fine for small datasets).
5. **No Task Editing**: Can create, complete, and delete tasks, but not edit existing task details.
6. **No Input Sanitization**: Frontend validation only; implement backend validation for production.
7. **Minimal Error Handling**: Basic error messages; enhance for production use.
8. **No Email Verification**: No email confirmation for new user registrations.
9. **No Task Due Dates**: Simple pending/completed status; no deadline tracking.
10. **Single Database**: No environment-specific configurations for dev/prod.
11. **Integer Primary Keys**: Currently using INT AUTO_INCREMENT for IDs. For production applications with large-scale data, migrate to UUID (CHAR(36)) or BIGINT to prevent integer overflow. UUID example: `id CHAR(36) PRIMARY KEY`.

## Technical Stack

- **Backend**: Flask 2.x, Python 3.7+
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Database**: MySQL 8.0+
- **API**: RESTful JSON API
- **Session Management**: Browser localStorage

## Styling & UI Theme

- **Primary Color**: Light Green (#66bb6a, #4caf50)
- **Accent Colors**: Mint Green (#c8e6c9), Red (#f44336)
- **Background**: Transparent blur effect for auth pages, light gray for main content
- **Design Pattern**: Card-based layouts with shadows and hover effects
- **Responsive**: Mobile-friendly design with media queries

## Resources & Documentation

### Official Documentation

- **Flask Documentation**: https://flask.palletsprojects.com/
- **MySQL Documentation**: https://dev.mysql.com/doc/
- **mysql-connector-python**: https://dev.mysql.com/doc/connector-python/en/
- **Flask-CORS**: https://flask-cors.readthedocs.io/
- **MDN Web Docs**: https://developer.mozilla.org/

### Learning Resources

- **Flask Tutorial**: https://flask.palletsprojects.com/tutorial/
- **JavaScript Fetch API**: https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API
- **CSS Grid & Flexbox**: https://css-tricks.com/
- **REST API Best Practices**: https://restfulapi.net/
- **Web Development Best Practices**: https://web.dev/

### Tools & Utilities

- **MySQL Workbench**: https://www.mysql.com/products/workbench/
- **Postman (API Testing)**: https://www.postman.com/
- **Git Documentation**: https://git-scm.com/doc
- **VS Code**: https://code.visualstudio.com/

## Troubleshooting

### Backend Won't Start

**Error**: `ModuleNotFoundError: No module named 'flask'`
- **Solution**: Install dependencies: `pip install -r requirements.txt`

**Error**: `Connection refused to MySQL server`
- **Solution**: Ensure MySQL is running: `mysql -u root -p`

### Frontend Won't Connect to Backend

**Error**: `Failed to fetch` or CORS error
- **Solution**: Ensure backend is running on `http://127.0.0.1:5000`
- Check that Flask app has CORS enabled: `CORS(app)`

### Login/Registration Issues

**Error**: "Error loading profile" or "Cannot read properties of null"
- **Solution**: Clear localStorage and try again:
  ```javascript
  localStorage.clear();
  ```

### Database Connection Failed

**Error**: `Access denied for user 'root'@'localhost'`
- **Solution**: Update credentials in `backend/db.py` with your MySQL username and password

### Tasks Not Showing

**Error**: "Error loading tasks" message
- **Solution**: 
  1. Verify backend is running
  2. Check network tab in browser DevTools
  3. Ensure user_id is stored in localStorage
  4. Verify database tables exist

## Future Enhancements

- [ ] Password Encryption (bcrypt/argon2)
- [ ] Task Due Dates and Reminders
- [ ] Task Priority Levels
- [ ] Task Categories/Tags
- [ ] User Settings & Preferences
- [ ] Password Reset via Email
- [ ] Task Search and Filtering
- [ ] Pagination for Tasks
- [ ] Dark Mode Toggle
- [ ] Export Tasks to CSV/PDF
- [ ] Mobile App (React Native)
- [ ] Collaborative Tasks (Team Sharing)
- [ ] Task History and Undo
- [ ] Notifications System



## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues, questions, or suggestions, please create an issue in the repository or contact the development team.

---

