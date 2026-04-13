from flask import Flask, make_response, request, jsonify
from flask_migrate import Migrate
from datetime import datetime

from models import *
from schemas import WorkoutSchema, ExerciseSchema, WorkoutExerciseSchema

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)
db.init_app(app)

# Initialize schemas
workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)
exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)
workout_exercise_schema = WorkoutExerciseSchema()


# ==================== WORKOUT ENDPOINTS ====================

@app.route('/workouts', methods=['GET'])
def get_workouts():
    """GET /workouts - List all workouts"""
    try:
        workouts = Workout.query.all()
        return make_response(workouts_schema.dump(workouts), 200)
    except Exception as e:
        return make_response(jsonify({'error': str(e)}), 500)


@app.route('/workouts/<int:id>', methods=['GET'])
def get_workout(id):
    """GET /workouts/<id> - Show a single workout with its associated exercises"""
    try:
        workout = Workout.query.get(id)
        if not workout:
            return make_response(jsonify({'error': 'Workout not found'}), 404)
        return make_response(workout_schema.dump(workout), 200)
    except Exception as e:
        return make_response(jsonify({'error': str(e)}), 500)


@app.route('/workouts', methods=['POST'])
def create_workout():
    """POST /workouts - Create a new workout"""
    try:
        data = request.get_json()
        errors = workout_schema.validate(data)
        if errors:
            return make_response(jsonify({'errors': errors}), 400)
        
        new_workout = workout_schema.load(data)
        db.session.add(new_workout)
        db.session.commit()
        return make_response(workout_schema.dump(new_workout), 201)
    except ValueError as e:
        db.session.rollback()
        return make_response(jsonify({'error': str(e)}), 400)
    except Exception as e:
        db.session.rollback()
        return make_response(jsonify({'error': str(e)}), 500)


@app.route('/workouts/<int:id>', methods=['DELETE'])
def delete_workout(id):
    """DELETE /workouts/<id> - Delete a workout and associated WorkoutExercises"""
    try:
        workout = Workout.query.get(id)
        if not workout:
            return make_response(jsonify({'error': 'Workout not found'}), 404)
        
        # Delete associated workout_exercises (cascade handled by model)
        db.session.delete(workout)
        db.session.commit()
        return make_response(jsonify({'message': 'Workout deleted successfully'}), 200)
    except Exception as e:
        db.session.rollback()
        return make_response(jsonify({'error': str(e)}), 500)


# ==================== EXERCISE ENDPOINTS ====================

@app.route('/exercises', methods=['GET'])
def get_exercises():
    """GET /exercises - List all exercises"""
    try:
        exercises = Exercise.query.all()
        return make_response(exercises_schema.dump(exercises), 200)
    except Exception as e:
        return make_response(jsonify({'error': str(e)}), 500)


@app.route('/exercises/<int:id>', methods=['GET'])
def get_exercise(id):
    """GET /exercises/<id> - Show an exercise and associated workouts"""
    try:
        exercise = Exercise.query.get(id)
        if not exercise:
            return make_response(jsonify({'error': 'Exercise not found'}), 404)
        return make_response(exercise_schema.dump(exercise), 200)
    except Exception as e:
        return make_response(jsonify({'error': str(e)}), 500)


@app.route('/exercises', methods=['POST'])
def create_exercise():
    """POST /exercises - Create a new exercise"""
    try:
        data = request.get_json()
        errors = exercise_schema.validate(data)
        if errors:
            return make_response(jsonify({'errors': errors}), 400)
        
        new_exercise = exercise_schema.load(data)
        db.session.add(new_exercise)
        db.session.commit()
        return make_response(exercise_schema.dump(new_exercise), 201)
    except ValueError as e:
        db.session.rollback()
        return make_response(jsonify({'error': str(e)}), 400)
    except Exception as e:
        db.session.rollback()
        return make_response(jsonify({'error': str(e)}), 500)


@app.route('/exercises/<int:id>', methods=['DELETE'])
def delete_exercise(id):
    """DELETE /exercises/<id> - Delete an exercise and associated WorkoutExercises"""
    try:
        exercise = Exercise.query.get(id)
        if not exercise:
            return make_response(jsonify({'error': 'Exercise not found'}), 404)
        
        # Delete associated workout_exercises (cascade handled by model)
        db.session.delete(exercise)
        db.session.commit()
        return make_response(jsonify({'message': 'Exercise deleted successfully'}), 200)
    except Exception as e:
        db.session.rollback()
        return make_response(jsonify({'error': str(e)}), 500)


# ==================== WORKOUT EXERCISE ENDPOINTS ====================

@app.route('/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises', methods=['POST'])
def add_exercise_to_workout(workout_id, exercise_id):
    """POST /workouts/<workout_id>/exercises/<exercise_id>/workout_exercises - Add an exercise to a workout"""
    try:
        # Verify workout exists
        workout = Workout.query.get(workout_id)
        if not workout:
            return make_response(jsonify({'error': 'Workout not found'}), 404)
        
        # Verify exercise exists
        exercise = Exercise.query.get(exercise_id)
        if not exercise:
            return make_response(jsonify({'error': 'Exercise not found'}), 404)
        
        data = request.get_json()
        # Add IDs to the data
        data['workout_id'] = workout_id
        data['exercise_id'] = exercise_id
        
        errors = workout_exercise_schema.validate(data)
        if errors:
            return make_response(jsonify({'errors': errors}), 400)
        
        new_workout_exercise = workout_exercise_schema.load(data)
        db.session.add(new_workout_exercise)
        db.session.commit()
        return make_response(workout_exercise_schema.dump(new_workout_exercise), 201)
    except ValueError as e:
        db.session.rollback()
        return make_response(jsonify({'error': str(e)}), 400)
    except Exception as e:
        db.session.rollback()
        error_msg = str(e)
        if 'already added' in error_msg.lower():
            return make_response(jsonify({'error': 'This exercise is already added to this workout'}), 400)
        return make_response(jsonify({'error': error_msg}), 500)


if __name__ == '__main__':
    app.run(port=5555, debug=True)
