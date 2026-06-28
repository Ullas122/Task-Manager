# API Testing Examples

## 1. Health Check

GET http://localhost:5000/health

## 2. Get All Tasks

GET http://localhost:5000/api/tasks

## 3. Get Tasks by Status

GET http://localhost:5000/api/tasks?status=pending

## 4. Get Tasks by Priority

GET http://localhost:5000/api/tasks?priority=high

## 5. Get Filtered Tasks (Status + Priority)

GET http://localhost:5000/api/tasks?status=in_progress&priority=high

## 6. Get Single Task

GET http://localhost:5000/api/tasks/1

## 7. Create New Task - High Priority

POST http://localhost:5000/api/tasks
Content-Type: application/json

{
"title": "Complete project report",
"description": "Finish the quarterly report for management",
"priority": "high",
"status": "in_progress",
"due_date": "2026-07-15T18:00:00"
}

## 8. Create New Task - Simple

POST http://localhost:5000/api/tasks
Content-Type: application/json

{
"title": "Buy groceries"
}

## 9. Update Task Status

PUT http://localhost:5000/api/tasks/1
Content-Type: application/json

{
"status": "completed"
}

## 10. Update Task Priority

PUT http://localhost:5000/api/tasks/1
Content-Type: application/json

{
"priority": "low"
}

## 11. Update Multiple Fields

PUT http://localhost:5000/api/tasks/1
Content-Type: application/json

{
"title": "Updated title",
"status": "completed",
"priority": "medium",
"description": "Updated description"
}

## 12. Delete Single Task

DELETE http://localhost:5000/api/tasks/1

## 13. Delete All Tasks

DELETE http://localhost:5000/api/tasks

---

## Using with Postman

1. Import these requests into Postman
2. Change host/port if using different configuration
3. Test each endpoint with provided examples
4. Modify request bodies as needed for your use case

## Using with cURL

### Example Commands:

```bash
# Health check
curl http://localhost:5000/health

# Get all tasks
curl http://localhost:5000/api/tasks

# Create task
curl -X POST http://localhost:5000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"title":"Test Task","priority":"high"}'

# Update task
curl -X PUT http://localhost:5000/api/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"status":"completed"}'

# Delete task
curl -X DELETE http://localhost:5000/api/tasks/1
```

## Using with JavaScript/Fetch API

```javascript
// Get all tasks
fetch("http://localhost:5000/api/tasks")
  .then((response) => response.json())
  .then((data) => console.log(data));

// Create task
fetch("http://localhost:5000/api/tasks", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    title: "New Task",
    priority: "high",
    description: "Task description",
  }),
})
  .then((response) => response.json())
  .then((data) => console.log(data));

// Update task
fetch("http://localhost:5000/api/tasks/1", {
  method: "PUT",
  headers: {
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    status: "completed",
  }),
})
  .then((response) => response.json())
  .then((data) => console.log(data));

// Delete task
fetch("http://localhost:5000/api/tasks/1", {
  method: "DELETE",
})
  .then((response) => response.json())
  .then((data) => console.log(data));
```
