# Cloud-Based Task Manager

A lightweight REST API web application for task management built with Python Flask and SQLite. Designed with modern API best practices and ready for cloud deployment.

## Features

- **RESTful API Design**: Full CRUD operations with GET, POST, PUT, DELETE endpoints
- **SQLite Database**: Lightweight, file-based database perfect for cloud deployment
- **Task Management**: Create, read, update, and delete tasks with priority and status tracking
- **Filtering**: Query tasks by status and priority
- **Error Handling**: Comprehensive error responses with appropriate HTTP status codes
- **Environment Configuration**: Secure setup with environment variables
- **Cloud Ready**: Configured for deployment on Render platform

## Technology Stack

- **Backend**: Python Flask 3.0.0
- **Database**: SQLite with SQLAlchemy ORM
- **Server**: Gunicorn WSGI HTTP Server
- **Deployment**: Render Cloud Platform

## Project Structure

```
task-manager/
├── app.py              # Main Flask application with routes
├── models.py           # Database models
├── config.py           # Configuration management
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variables template
├── render.yaml         # Render deployment configuration
└── README.md           # This file
```

## Installation

### Local Development

1. **Clone the repository** (or create it from the structure above)

2. **Create and activate virtual environment**:

   ```bash
   python -m venv venv

   # On Windows
   venv\Scripts\activate

   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:

   ```bash
   cp .env.example .env
   ```

5. **Run the application**:

   ```bash
   python app.py
   ```

   The API will be available at `http://localhost:5000`

## API Endpoints

### Health Check

- **GET** `/health` - Check if the API is running
  ```bash
  curl http://localhost:5000/health
  ```

### Tasks

#### Get All Tasks

- **GET** `/api/tasks` - Retrieve all tasks

  ```bash
  curl http://localhost:5000/api/tasks
  ```

- **Query Parameters**:
  - `status`: Filter by status (pending, in_progress, completed)
  - `priority`: Filter by priority (low, medium, high)

  ```bash
  curl "http://localhost:5000/api/tasks?status=pending&priority=high"
  ```

#### Get Single Task

- **GET** `/api/tasks/<id>` - Get a specific task by ID
  ```bash
  curl http://localhost:5000/api/tasks/1
  ```

#### Create Task

- **POST** `/api/tasks` - Create a new task
  ```bash
  curl -X POST http://localhost:5000/api/tasks \
    -H "Content-Type: application/json" \
    -d '{
      "title": "Complete project",
      "description": "Finish the Flask API",
      "priority": "high",
      "status": "in_progress",
      "due_date": "2026-07-15T18:00:00"
    }'
  ```

**Request Body**:

```json
{
  "title": "Task title (required)",
  "description": "Task description (optional)",
  "status": "pending|in_progress|completed (default: pending)",
  "priority": "low|medium|high (default: medium)",
  "due_date": "ISO format datetime (optional)"
}
```

#### Update Task

- **PUT** `/api/tasks/<id>` - Update an existing task
  ```bash
  curl -X PUT http://localhost:5000/api/tasks/1 \
    -H "Content-Type: application/json" \
    -d '{
      "status": "completed",
      "priority": "low"
    }'
  ```

#### Delete Task

- **DELETE** `/api/tasks/<id>` - Delete a specific task
  ```bash
  curl -X DELETE http://localhost:5000/api/tasks/1
  ```

#### Delete All Tasks

- **DELETE** `/api/tasks` - Delete all tasks
  ```bash
  curl -X DELETE http://localhost:5000/api/tasks
  ```

## Response Examples

### Success Response (200 OK)

```json
{
  "id": 1,
  "title": "Complete project",
  "description": "Finish the Flask API",
  "status": "in_progress",
  "priority": "high",
  "due_date": "2026-07-15T18:00:00",
  "created_at": "2026-06-28T10:30:00",
  "updated_at": "2026-06-28T11:45:00"
}
```

### Error Response (400 Bad Request)

```json
{
  "error": "Title is required"
}
```

## Environment Variables

Create a `.env` file in the root directory (copy from `.env.example`):

```
FLASK_ENV=development        # Set to 'production' for cloud deployment
DATABASE_URL=sqlite:///tasks.db  # Database connection string
PORT=5000                    # Server port
```

## Deployment on Render

### Quick Deploy Steps

1. **Sign up on [Render.com](https://render.com)**

2. **Connect your GitHub repository**

3. **Create a new Web Service**:
   - Select Python as runtime
   - Build command: `pip install -r requirements.txt`
   - Start command: `gunicorn app:app`

4. **Add environment variables**:
   - Go to Environment
   - Add `FLASK_ENV=production`
   - Add other necessary variables from `.env.example`

5. **Deploy**:
   - Render will automatically build and deploy your service
   - Your API will be available at `https://your-service-name.onrender.com`

### Alternative: Using render.yaml

If using the `render.yaml` configuration file:

1. Push to GitHub
2. Go to Render Dashboard
3. Select "New +" → "Blueprint"
4. Connect your repository
5. Render will read `render.yaml` and deploy accordingly

## Database Schema

### Tasks Table

| Column      | Type        | Description                   |
| ----------- | ----------- | ----------------------------- |
| id          | Integer     | Primary key, auto-increment   |
| title       | String(255) | Task title (required)         |
| description | Text        | Task description (optional)   |
| status      | String(20)  | pending/in_progress/completed |
| priority    | String(10)  | low/medium/high               |
| due_date    | DateTime    | Task due date (optional)      |
| created_at  | DateTime    | Timestamp when created        |
| updated_at  | DateTime    | Timestamp of last update      |

## Testing the API

### Using cURL

```bash
# Create a task
curl -X POST http://localhost:5000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"title":"Test Task","priority":"high"}'

# Get all tasks
curl http://localhost:5000/api/tasks

# Update a task
curl -X PUT http://localhost:5000/api/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"status":"completed"}'

# Delete a task
curl -X DELETE http://localhost:5000/api/tasks/1
```

### Using Postman

1. Import the collection from the endpoints listed above
2. Set the base URL to `http://localhost:5000` for local testing
3. Test each endpoint with different parameters

## Production Considerations

1. **Database**: Consider migrating to PostgreSQL for production use
   - Update `DATABASE_URL` to PostgreSQL connection string
   - Render supports PostgreSQL databases

2. **Security**:
   - Add authentication/authorization (JWT tokens)
   - Implement rate limiting
   - Add CORS configuration as needed
   - Use HTTPS (Render provides this by default)

3. **Monitoring**:
   - Set up logging
   - Monitor error rates
   - Track performance metrics

4. **Scaling**:
   - Switch to a paid Render plan for better performance
   - Use PostgreSQL instead of SQLite for concurrent access
   - Implement caching with Redis

## Troubleshooting

### Port Already in Use

```bash
# Change PORT in .env or run on different port
python app.py --port 5001
```

### Database Lock Error (SQLite)

- Occurs with concurrent writes
- Solution: Migrate to PostgreSQL for production

### Module Not Found

```bash
# Ensure virtual environment is activated
pip install -r requirements.txt
```

## Future Enhancements

- [ ] User authentication and authorization
- [ ] Task categories/projects
- [ ] Task assignments to users
- [ ] Email notifications for due tasks
- [ ] Task dependencies
- [ ] Recurring tasks
- [ ] Task attachments
- [ ] API documentation (Swagger/OpenAPI)
- [ ] Unit and integration tests
- [ ] WebSocket support for real-time updates

## License

MIT License - Feel free to use this project for personal or commercial purposes

## Support

For issues, questions, or suggestions, please open an issue on GitHub or contact the development team.

---

**Happy task managing!** 🚀
