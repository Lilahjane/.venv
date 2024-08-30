from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define the database models
class Announcement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50))
    title = db.Column(db.String(200))
    description = db.Column(db.String(200))
    due_date = db.Column(db.String(50))
    due_time = db.Column(db.String(50))
    attachments = db.Column(db.String(200))
    links = db.Column(db.String(200))
    assignment = db.Column(db.String(50))
    max_points = db.Column(db.String(50))
    item_id = db.Column(db.String(50))
    post_id = db.Column(db.String(50))
    alternate_link = db.Column(db.String(200))
    teacher = db.Column(db.String(100))
    course = db.Column(db.String(100))
    assignment_link = db.Column(db.String(200))

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipe_name = db.Column(db.String(200))
    recipe_photo = db.Column(db.String(200))
    recipe_url = db.Column(db.String(200))
    calories = db.Column(db.String(50))
    carbohydrates = db.Column(db.String(50))
    net_carbs = db.Column(db.String(50))
    fat = db.Column(db.String(50))
    protein = db.Column(db.String(50))
    sodium = db.Column(db.String(50))
    prep_time = db.Column(db.String(50))
    difficulty_level = db.Column(db.String(50))
    spice_level = db.Column(db.String(50))
    ingredients = db.Column(db.Text)  # Will store ingredients as JSON string

# Create the database tables
with app.app_context():
    db.create_all()

def load_combined_data():
    with open('combined_data.json') as f:
        data = json.load(f)
        for item in data:
            announcement = Announcement(
                type=item['Type'],
                title=item['Title'],
                description=item['Description'],
                due_date=item['Due_Date'],
                due_time=item['Due_Time'],
                attachments=item['Attachments'],
                links=item['Links'],
                assignment=item['Assignment'],
                max_points=item['Max_Points'],
                item_id=item['Item_ID'],
                post_id=item['Post_ID'],
                alternate_link=item['Alternate_Link'],
                teacher=item['Teacher'],
                course=item['Course'],
                assignment_link=item['Assignment_Link']
            )
            db.session.add(announcement)
        db.session.commit()

def load_source_data():
    with open('source.json') as f:
        data = json.load(f)
        for item in data:
            recipe = Recipe(
                recipe_name=item['recipe_name'],
                recipe_photo=item['recipe_photo'],
                recipe_url=item['recipe_url'],
                calories=item['Calories'],
                carbohydrates=item['Carbohydrates'],
                net_carbs=item['Net_Carbs'],
                fat=item['Fat'],
                protein=item['Protein'],
                sodium=item['Sodium'],
                prep_time=item['Prep_Time'],
                difficulty_level=item['Difficulty_Level'],
                spice_level=item['Spice_Level'],
                ingredients=json.dumps(item['Ingredients'])  # Store as JSON string
            )
            db.session.add(recipe)
        db.session.commit()

# Root route
@app.route('/')
def home():
    return "Welcome to the Flask API! Available endpoints: /announcements, /recipes"

@app.route('/announcements', methods=['GET'])
def get_announcements():
    announcements = Announcement.query.all()
    return jsonify([{
        'id': a.id,
        'type': a.type,
        'title': a.title,
        'description': a.description,
        'teacher': a.teacher,
        'course': a.course,
        'due_date': a.due_date,
        'due_time': a.due_time,
        'attachments': a.attachments,
        'links': a.links,
        'assignment': a.assignment,
        'max_points': a.max_points,
        'item_id': a.item_id,
        'post_id': a.post_id,
        'alternate_link': a.alternate_link,
        'teacher': a.teacher,
        'course': a.course,
        'assignment_link': a.assignment_link
        # Add other fields as needed
    } for a in announcements])

@app.route('/recipes', methods=['GET'])
def get_recipes():
    recipes = Recipe.query.all()
    return jsonify([{
        'id': r.id,
        'recipe_name': r.recipe_name,
        'recipe_url': r.recipe_url,
        
        # Add other fields as needed
    } for r in recipes])

if __name__ == '__main__':
    with app.app_context():
        # Load data into the database
        load_combined_data()
        load_source_data()
    app.run(debug=True)
