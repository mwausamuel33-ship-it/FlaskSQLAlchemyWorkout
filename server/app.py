# app.py - all routes live here
# TODO: maybe use blueprints later if this gets too long

from flask import Flask, request
from flask_migrate import Migrate
from models import *
from schemas import WorkoutSchema, ExerciseSchema, WorkoutExerciseSchema

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # stops a warning

migrate = Migrate(app, db)
db.init_app(app)

# schema instances (many=True is for lists)
workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)
exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)
workout_exercise_schema = WorkoutExerciseSchema()


# -- ROOT ROUTE --

@app.route('/', methods=['GET'])
def home():
    return {
        'message': 'Workout Tracker API',
        'version': '1.0',
        'endpoints': {
            'workouts': {
                'GET /workouts': 'Get all workouts',
                'GET /workouts/<id>': 'Get specific workout',
                'POST /workouts': 'Create new workout',
                'PATCH /workouts/<id>': 'Update workout',
                'DELETE /workouts/<id>': 'Delete workout',
            },
            'exercises': {
                'GET /exercises': 'Get all exercises',
                'GET /exercises/<id>': 'Get specific exercise',
                'POST /exercises': 'Create new exercise',
                'PATCH /exercises/<id>': 'Update exercise',
                'DELETE /exercises/<id>': 'Delete exercise',
            },
            'workout_exercises': {
                'GET /workouts/<workout_id>/exercises': 'Get exercises in workout',
                'GET /workouts/<workout_id>/exercises/<exercise_id>/workout_exercises': 'Get specific workout exercise',
                'POST /workouts/<workout_id>/exercises/<exercise_id>/workout_exercises': 'Add exercise to workout',
                'PATCH /workouts/<workout_id>/exercises/<exercise_id>/workout_exercises': 'Update exercise in workout',
            }
        }
    }, 200


# -- WORKOUT ROUTES --

@app.route('/workouts', methods=['GET'])
def get_workouts():
    try:
        all_workouts = Workout.query.all()
        return workouts_schema.dump(all_workouts), 200
    except Exception as e:
        return {'error': f'Failed to fetch workouts: {str(e)}'}, 500


@app.route('/workouts/<int:id>', methods=['GET'])
def get_workout(id):
    workout = Workout.query.get(id)
    if workout == None:
        return {'error': f'Workout not found with id {id}'}, 404
    return workout_schema.dump(workout), 200


@app.route('/workouts', methods=['POST'])
def create_workout():
    data = request.get_json()
    if data == None:
        return {'error': 'No data provided. Expected JSON body with date, duration_minutes, and optional notes'}, 400

    errors = workout_schema.validate(data)
    if len(errors) > 0:
        return {'errors': errors}, 400

    try:
        loaded_data = workout_schema.load(data)
        new_workout = Workout(**loaded_data)
        db.session.add(new_workout)
        db.session.commit()
        return workout_schema.dump(new_workout), 201
    except Exception as e:
        db.session.rollback()
        return {'error': f'Failed to create workout: {str(e)}'}, 400


@app.route('/workouts/<int:id>', methods=['PATCH'])
def update_workout(id):
    workout = Workout.query.get(id)
    if workout == None:
        return {'error': f'Workout not found with id {id}'}, 404
    
    data = request.get_json()
    if data == None:
        return {'error': 'No data provided'}, 400
    
    # validate only the fields being updated
    errors = workout_schema.validate(data, partial=True)
    if len(errors) > 0:
        return {'errors': errors}, 400
    
    try:
        # load with partial=True to allow partial updates
        updated_data = workout_schema.load(data, partial=True)
        for key, value in updated_data.items():
            setattr(workout, key, value)
        db.session.commit()
        return workout_schema.dump(workout), 200
    except Exception as e:
        db.session.rollback()
        return {'error': f'Failed to update workout: {str(e)}'}, 400


@app.route('/workouts/<int:id>', methods=['DELETE'])
def delete_workout(id):
    workout = Workout.query.get(id)
    if workout == None:
        return {'error': f'Workout not found with id {id}'}, 404
    try:
        db.session.delete(workout)
        db.session.commit()
        return {'message': f'Workout {id} deleted successfully'}, 200
    except Exception as e:
        db.session.rollback()
        return {'error': f'Failed to delete workout: {str(e)}'}, 400


# -- EXERCISE ROUTES --

@app.route('/exercises', methods=['GET'])
def get_exercises():
    try:
        all_exercises = Exercise.query.all()
        return exercises_schema.dump(all_exercises), 200
    except Exception as e:
        return {'error': f'Failed to fetch exercises: {str(e)}'}, 500


@app.route('/exercises/<int:id>', methods=['GET'])
def get_exercise(id):
    exercise = Exercise.query.get(id)
    if exercise == None:
        return {'error': f'Exercise not found with id {id}'}, 404
    return exercise_schema.dump(exercise), 200


@app.route('/exercises', methods=['POST'])
def create_exercise():
    data = request.get_json()
    if data == None:
        return {'error': 'No data provided. Expected JSON body with name, category, and optional equipment_needed'}, 400

    errors = exercise_schema.validate(data)
    if len(errors) > 0:
        return {'errors': errors}, 400

    try:
        loaded_data = exercise_schema.load(data)
        new_exercise = Exercise(**loaded_data)
        db.session.add(new_exercise)
        db.session.commit()
        return exercise_schema.dump(new_exercise), 201
    except Exception as e:
        db.session.rollback()
        return {'error': f'Failed to create exercise: {str(e)}'}, 400


@app.route('/exercises/<int:id>', methods=['PATCH'])
def update_exercise(id):
    exercise = Exercise.query.get(id)
    if exercise == None:
        return {'error': f'Exercise not found with id {id}'}, 404
    
    data = request.get_json()
    if data == None:
        return {'error': 'No data provided'}, 400
    
    # validate only the fields being updated
    errors = exercise_schema.validate(data, partial=True)
    if len(errors) > 0:
        return {'errors': errors}, 400
    
    try:
        # load with partial=True to allow partial updates
        updated_data = exercise_schema.load(data, partial=True)
        for key, value in updated_data.items():
            setattr(exercise, key, value)
        db.session.commit()
        return exercise_schema.dump(exercise), 200
    except Exception as e:
        db.session.rollback()
        return {'error': f'Failed to update exercise: {str(e)}'}, 400


@app.route('/exercises/<int:id>', methods=['DELETE'])
def delete_exercise(id):
    exercise = Exercise.query.get(id)
    if exercise == None:
        return {'error': f'Exercise not found with id {id}'}, 404
    try:
        db.session.delete(exercise)
        db.session.commit()
        return {'message': f'Exercise {id} deleted successfully'}, 200
    except Exception as e:
        db.session.rollback()
        return {'error': f'Failed to delete exercise: {str(e)}'}, 400


# -- WORKOUT EXERCISE ROUTES --
# adds an exercise to a workout (creates a row in the join table)

@app.route('/workouts/<int:workout_id>/exercises', methods=['GET'])
def get_workout_exercises(workout_id):
    workout = Workout.query.get(workout_id)
    if workout == None:
        return {'error': f'Workout not found with id {workout_id}'}, 404
    
    try:
        workout_exercises = WorkoutExercise.query.filter_by(workout_id=workout_id).all()
        return [workout_exercise_schema.dump(we) for we in workout_exercises], 200
    except Exception as e:
        return {'error': f'Failed to fetch workout exercises: {str(e)}'}, 500


@app.route(
    '/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises',
    methods=['GET']
)
def get_workout_exercise(workout_id, exercise_id):
    we = WorkoutExercise.query.filter_by(
        workout_id=workout_id,
        exercise_id=exercise_id
    ).first()
    
    if we == None:
        return {'error': f'No workout exercise found linking workout {workout_id} and exercise {exercise_id}'}, 404
    
    return workout_exercise_schema.dump(we), 200


@app.route(
    '/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises',
    methods=['POST']
)
def add_exercise_to_workout(workout_id, exercise_id):
    # make sure both exist before linking them
    if Workout.query.get(workout_id) == None:
        return {'error': 'Workout not found with id ' + str(workout_id)}, 404
    if Exercise.query.get(exercise_id) == None:
        return {'error': 'Exercise not found with id ' + str(exercise_id)}, 404

    data = request.get_json()
    if data == None:
        data = {}

    # inject ids from url into the data dict
    data['workout_id'] = workout_id
    data['exercise_id'] = exercise_id

    errors = workout_exercise_schema.validate(data)
    if len(errors) > 0:
        return {'errors': errors}, 400

    try:
        loaded_data = workout_exercise_schema.load(data)
        new_we = WorkoutExercise(**loaded_data)
        db.session.add(new_we)
        db.session.commit()
        return workout_exercise_schema.dump(new_we), 201
    except Exception as e:
        db.session.rollback()
        return {'error': f'Failed to add exercise to workout: {str(e)}'}, 400


@app.route(
    '/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises',
    methods=['PATCH']
)
def update_workout_exercise(workout_id, exercise_id):
    # find the workout exercise linking these two
    we = WorkoutExercise.query.filter_by(
        workout_id=workout_id,
        exercise_id=exercise_id
    ).first()
    
    if we == None:
        return {'error': f'No workout exercise found linking workout {workout_id} and exercise {exercise_id}'}, 404
    
    data = request.get_json()
    if data == None:
        return {'error': 'No data provided'}, 400
    
    # validate only the fields being updated
    errors = workout_exercise_schema.validate(data, partial=True)
    if len(errors) > 0:
        return {'errors': errors}, 400
    
    try:
        # load with partial=True to allow partial updates
        updated_data = workout_exercise_schema.load(data, partial=True)
        for key, value in updated_data.items():
            # skip workout_id and exercise_id since they can't be changed
            if key not in ['workout_id', 'exercise_id']:
                setattr(we, key, value)
        db.session.commit()
        return workout_exercise_schema.dump(we), 200
    except Exception as e:
        db.session.rollback()
        return {'error': f'Failed to update workout exercise: {str(e)}'}, 400


if __name__ == '__main__':
    app.run(debug=True, port=5555)
