# Django Kanban Project

A dockerized Django project with a beautiful kanban board for managing daily tasks.

## Prerequisites

- Docker
- Docker Compose

## Quick Start

1. **Copy the environment file:**
   ```bash
   cp .env.example .env
   ```

2. **Build and start the containers:**
   ```bash
   docker-compose up --build
   ```

3. **Run migrations (in a new terminal):**
   ```bash
   docker-compose exec web python manage.py migrate
   ```

4. **Create a superuser (optional):**
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

5. **Access the application:**
   - Kanban Board: http://localhost:8000 (home page)
   - Admin panel: http://localhost:8000/admin

## Development

### Running Commands

To run Django management commands:
```bash
docker-compose exec web python manage.py <command>
```

### Creating a New App

```bash
docker-compose exec web python manage.py startapp <app_name>
```

### Accessing the Database

The PostgreSQL database is accessible at:
- Host: localhost
- Port: 5432
- Database: canban_db
- User: canban_user
- Password: canban_password

## Features

- **Kanban Board**: Drag-and-drop task management with three columns (To Do, In Progress, Done)
- **Task Management**: Create, edit, and delete tasks with priorities and due dates
- **Modern UI**: Beautiful, responsive design with smooth animations
- **Priority Levels**: Low, Medium, and High priority indicators
- **Due Dates**: Track task deadlines with overdue highlighting

## Project Structure

```
canban/
├── canban/          # Django project settings
├── tasks/           # Kanban board app
│   ├── models.py    # Task model
│   ├── views.py     # Task views
│   ├── templates/   # HTML templates
│   └── static/      # CSS styles
├── manage.py        # Django management script
├── requirements.txt # Python dependencies
├── Dockerfile       # Docker image configuration
├── docker-compose.yml # Docker Compose configuration
└── README.md        # This file
```

## Environment Variables

Edit `.env` file to configure:
- `DEBUG`: Set to 1 for development, 0 for production
- `SECRET_KEY`: Django secret key (change in production!)
- `DATABASE_URL`: PostgreSQL connection string
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts

## Stopping the Containers

```bash
docker-compose down
```

To remove volumes (database data):
```bash
docker-compose down -v
```

## Deployment on Railway

This project is configured to deploy on Railway. Here's how:

### Prerequisites
- Railway account (sign up at https://railway.app)
- Railway CLI (optional, for local testing)

### Steps

1. **Create a new Railway project:**
   - Go to Railway dashboard
   - Click "New Project"
   - Select "Deploy from GitHub repo" or "Empty Project"

2. **Add PostgreSQL database:**
   - In your Railway project, click "New"
   - Select "Database" → "Add PostgreSQL"
   - Railway will automatically create a `DATABASE_URL` environment variable

3. **Deploy your application:**
   - If deploying from GitHub, connect your repository
   - Railway will automatically detect the Dockerfile and build your app
   - Or use Railway CLI: `railway up`

4. **Set environment variables:**
   - Go to your service → Variables
   - Add the following variables:
     - `SECRET_KEY`: Generate a secure key (e.g., using `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`)
     - `DEBUG`: Set to `0` for production
     - `ALLOWED_HOSTS`: Your Railway domain (e.g., `your-app.railway.app`)
   - Note: `DATABASE_URL` is automatically set by Railway when you add PostgreSQL

5. **The application will automatically:**
   - Run migrations on startup
   - Collect static files
   - Start the Django server

### Railway Configuration

The project includes:
- `railway.json`: Railway-specific configuration
- `start.sh`: Startup script that runs migrations and starts the server
- `Dockerfile`: Configured to use Railway's `PORT` environment variable

### Troubleshooting

If you encounter database connection errors:
- Ensure PostgreSQL service is running in Railway
- Check that `DATABASE_URL` is set correctly
- Verify the database is accessible from your service

If static files aren't loading:
- Check that `collectstatic` ran successfully in the build logs
- Verify `STATIC_ROOT` is set correctly in settings.py

