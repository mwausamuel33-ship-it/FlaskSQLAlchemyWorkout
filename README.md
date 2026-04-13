# Workout Tracker API

This is my Flask + SQLAlchemy project for tracking workouts and exercises. I built this as part of my backend development learning. It's a REST API that lets you create workouts, add exercises to them, and track reps/sets/duration.

Took me a while to get the relationships working but I think I got it 😅

---

## How to set it up

Make sure you have pipenv installed first. Then run:

```bash
pipenv install
pipenv shell
```

Then go into the server folder and run the migrations and seed the database:

```bash
cd server
flask db upgrade
python seed.py
```

> Note: if flask db upgrade gives you an error, try deleting the app.db file and migrations/versions folder and running `flask db init` and `flask db migrate` first. That fixed it for me.

---

## How to run it

```bash
flask run --port 5555
```

or just run app.py directly:

```bash
python app.py
```

The server will start on `http://localhost:5555`

---

## Endpoints

Here are all the routes. Full CRUD operations are now supported!

### Workouts

| Method | Route | What it does |
|--------|-------|--------------|
| GET | `/workouts` | get all workouts |
| GET | `/workouts/<id>` | get one workout by its id |
| POST | `/workouts` | create a new workout |
| PATCH | `/workouts/<id>` | update a workout (partial update) |
| DELETE | `/workouts/<id>` | delete a workout |

**POST/PATCH body example:**
```json
{
  "date": "2024-04-10",
  "duration_minutes": 45,
  "notes": "leg day"
}
```

> Note: For PATCH, you only need to include the fields you want to update

### Exercises

| Method | Route | What it does |
|--------|-------|--------------|
| GET | `/exercises` | get all exercises |
| GET | `/exercises/<id>` | get one exercise by id |
| POST | `/exercises` | create a new exercise |
| PATCH | `/exercises/<id>` | update an exercise (partial update) |
| DELETE | `/exercises/<id>` | delete an exercise |

**POST/PATCH body example:**
```json
{
  "name": "Bench Press",
  "category": "strength",
  "equipment_needed": true
}
```

> The category field only accepts: `strength`, `cardio`, `flexibility`, or `balance` — it'll give you a 400 error if you use something else (learned that the hard way)
> 
> For PATCH, you only need to include the fields you want to update

### Workout Exercises (the join table)

This one was the hardest part. It links a workout to an exercise and stores reps/sets/duration.

| Method | Route | What it does |
|--------|-------|--------------|
| GET | `/workouts/<workout_id>/exercises` | get all exercises in a workout |
| GET | `/workouts/<workout_id>/exercises/<exercise_id>/workout_exercises` | get details of a specific exercise in a workout |
| POST | `/workouts/<workout_id>/exercises/<exercise_id>/workout_exercises` | add an exercise to a workout |
| PATCH | `/workouts/<workout_id>/exercises/<exercise_id>/workout_exercises` | update exercise details in a workout (reps/sets/duration) |

**POST/PATCH body example:**
```json
{
  "reps": 12,
  "sets": 3
}
```

> For PATCH, you only need to include the fields you want to update. You can update reps, sets, and duration_seconds

---

## Quick test with curl

```bash
# get all exercises
curl http://localhost:5555/exercises

# create an exercise
curl -X POST http://localhost:5555/exercises \
  -H "Content-Type: application/json" \
  -d '{"name": "Bench Press", "category": "strength", "equipment_needed": true}'

# get all workouts
curl http://localhost:5555/workouts
```

---

## Models

I have 3 models:

- **Exercise** - stores exercise name, category, and whether equipment is needed
- **Workout** - stores date, duration, and notes
- **WorkoutExercise** - the join table between workouts and exercises, also stores reps/sets/duration_seconds

The relationship is many-to-many: a workout can have many exercises and an exercise can be in many workouts. WorkoutExercise is the association table that sits in the middle.

---

## Tech used

- Python 3
- Flask
- Flask-SQLAlchemy
- Flask-Migrate (for database migrations)
- Marshmallow (for serialization/validation — this was new to me)
- SQLite (for the database, just a local file)

---

## Features Implemented

- [x] Create (POST) endpoints for workouts, exercises, and workout-exercise links
- [x] Read (GET) endpoints for all resources
- [x] Update (PATCH) endpoints for workouts, exercises, and workout-exercise links
- [x] Delete (DELETE) endpoints for workouts and exercises
- [x] Comprehensive error handling and detailed error messages
- [x] Input validation using Marshmallow schemas
- [x] Database constraints for data integrity

## Future Features

- [ ] Authentication so different users can track their own workouts
- [ ] Frontend dashboard for visualizing workouts and progress
- [ ] Ability to search and filter workouts/exercises
- [ ] Statistics and analytics (total volume, frequency, etc.)
- [ ] User profiles and social features
