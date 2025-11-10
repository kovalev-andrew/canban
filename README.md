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

