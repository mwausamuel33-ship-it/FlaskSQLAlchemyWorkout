# Workout Tracking API

A Flask-based backend API for tracking workouts and exercises. This application allows personal trainers to create workouts, manage exercises, and track exercise details including sets, reps, and duration.

## Project Description

The Workout Tracking API is a RESTful backend service that manages:
- **Workouts**: Collections of exercises performed on a specific date
- **Exercises**: Reusable exercise templates with categories and equipment requirements
- **Workout Exercises**: Association between workouts and exercises with specific set/rep/duration data

The API includes comprehensive validation at the table, model, and schema levels to ensure data integrity and consistency.

## Installation

### Prerequisites
- Python 3.11+
- Pipenv

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd FlaskSQLAlchemyWorkout
```

2. Install dependencies:
```bash
pipenv install
```

3. Activate the virtual environment:
```bash
pipenv shell
```

4. Initialize the database:
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade head
```

5. Seed the database with sample data:
```bash
python seed.py
```

## Running the Application

Start the Flask development server:
```bash
flask run
```

The API will be available at `http://localhost:5555`

## API Endpoints

### Workouts

- **GET /workouts**
  - Lists all workouts
  - Returns: Array of workout objects with associated exercises

- **GET /workouts/<id>**
  - Shows a single workout with its associated exercises
  - Returns: Workout object with exercise details (reps/sets/duration)

- **POST /workouts**
  - Creates a new workout
  - Request body: `{ "date": "YYYY-MM-DD", "duration_minutes": int, "notes": string }`
  - Returns: Created workout object

- **DELETE /workouts/<id>**
  - Deletes a workout and associated WorkoutExercises
  - Returns: Success message

### Exercises

- **GET /exercises**
  - Lists all exercises
  - Returns: Array of exercise objects

- **GET /exercises/<id>**
  - Shows a single exercise with associated workouts
  - Returns: Exercise object with workouts

- **POST /exercises**
  - Creates a new exercise
  - Request body: `{ "name": string, "category": string, "equipment_needed": boolean }`
  - Returns: Created exercise object

- **DELETE /exercises/<id>**
  - Deletes an exercise and associated WorkoutExercises
  - Returns: Success message

### Workout Exercises

- **POST /workouts/<workout_id>/exercises/<exercise_id>/workout_exercises**
  - Adds an exercise to a workout with specific set/rep/duration data
  - Request body: `{ "reps": int, "sets": int, "duration_seconds": int }`
  - Returns: Created WorkoutExercise object

## Testing

Test the API using curl, Postman, or Flask shell:

```bash
flask shell
```

Inside the Flask shell, test relationships and validations:
```python
from models import *

# View all workouts
Workout.query.all()

# Create and test validations
exercise = Exercise(name="", category="cardio", equipment_needed=False)
db.session.add(exercise)
db.session.commit()  # Will raise validation error
```

## Project Structure

```
server/
├── app.py           # Flask application and route definitions
├── models.py        # SQLAlchemy models with validations
├── schemas.py       # Marshmallow schemas for serialization
└── seed.py          # Database seeding script
```

## Validations

### Table Constraints
- Workout: `date` is required and unique per day
- Exercise: `name` is required and unique
- WorkoutExercise: `workout_id` and `exercise_id` are required with foreign key constraints

### Model Validations
- Workout: duration_minutes must be positive
- Exercise: name cannot be empty, category must be from allowed values
- WorkoutExercise: reps, sets, and duration_seconds cannot be negative

### Schema Validations
- All required fields must be present
- Data types are validated and coerced
- Numeric fields must be positive integers

## Technologies Used

- **Flask 2.2.2**: Web framework
- **SQLAlchemy 3.0.3**: ORM
- **Flask-Migrate 3.1.0**: Database migrations
- **Marshmallow 3.20.1**: Serialization/deserialization
- **SQLite**: Database
