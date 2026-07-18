# Hostel Management System

A PHP + MySQL web app for hostel room allocation, developed by Pooja Meena (Computer Engineering Student, NIT KURUKSHETRA).

## Stack
- **Backend:** PHP 8.2 (built-in development server)
- **Database:** MySQL 8.0
- **Frontend:** Plain HTML/CSS/JS with PHP templates

## How to run

The workflow **"Start application"** handles everything automatically:
1. Initializes the MySQL data directory (first run only)
2. Starts the MySQL server on port 3306
3. Creates the `hostel_management_system` database and loads all schema/seed SQL files (first run only)
4. Starts the PHP built-in server on port 5000

Just press **Run** — no manual setup needed.

## Key files

| File/Dir | Purpose |
|---|---|
| `start.sh` | Startup script: MySQL init + PHP server |
| `includes/config.inc.php` | DB connection settings |
| `database/*.sql` | Schema and seed data for each table |
| `index.php` | Student login page (app entry point) |
| `login-hostel_manager.php` | Hostel Manager / Admin login |
| `admin/` | Admin panel pages |

## Database connection

Configured in `includes/config.inc.php`:
- Host: `127.0.0.1`
- User: `root` / Password: `root`
- Database: `hostel_management_system`

MySQL data lives in `/home/runner/mysql-data/` (persisted across restarts).

## User preferences
- Keep existing PHP/MySQL stack as-is
