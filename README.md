# Workout Tracker API

REST API backend for tracking workouts and exercises, built with Flask, SQLAlchemy, and Marshmallow.

## Description
This API enables personal trainers to create and manage workouts with associated exercises. Exercises are reusable across workouts, with support for tracking reps, sets, and duration for each exercise in a workout.

## Installation

1. Clone the repository
2. Install dependencies:
```bash
pipenv install
```
3. Initialize database:
```bash
cd server
flask db init
flask db upgrade
```
4. Seed database with sample data:
```bash
python seed.py
```

## Run the application
```bash
cd server
python app.py
```
Application runs on `http://localhost:5555`

## API Endpoints

### Workouts
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/workouts` | List all workouts |
| GET | `/workouts/<id>` | Get single workout with associated exercises |
| POST | `/workouts` | Create new workout |
| DELETE | `/workouts/<id>` | Delete workout and associated workout exercises |

### Exercises
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/exercises` | List all exercises |
| GET | `/exercises/<id>` | Get single exercise with associated workouts |
| POST | `/exercises` | Create new exercise |
| DELETE | `/exercises/<id>` | Delete exercise and associated workout exercises |

### Workout Exercises
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/workouts/<workout_id>/exercises/<exercise_id>/workout_exercises` | Add exercise to workout with reps/sets/duration |

## Validations
### Table Constraints
- Unique constraint: workout_id + exercise_id (cannot add same exercise to workout multiple times)
- Check constraints: reps, sets, duration_seconds must be positive when provided

### Model Validations
- Workout duration must be positive
- Exercise name must be at least 2 characters
- Exercise category must be one of: strength, cardio, flexibility, endurance, other
- WorkoutExercise numeric values must be positive

### Schema Validations
- Exercise name length between 2-255 characters
- Exercise category validation against allowed values
- WorkoutExercise requires at least one of reps/sets/duration_seconds
