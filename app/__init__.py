import os
import re
import datetime
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from peewee import *
from playhouse.shortcuts import model_to_dict

HOBBIES = [
    {
        'name': 'Programming',
        'images': [
            './static/img/coding3.jpg',
            './static/img/coding1.jpg',
            './static/img/coding2.jpg'
        ],
        'alt': 'Programming'
    },
    {
        'name': 'Gaming',
        'images': [
            './static/img/eafc.jpg',
            './static/img/cod.jpg',
            './static/img/reddead.jpg'
        ],
        'alt': 'Gaming'
    },
    {
        'name': 'Cooking',
        'images': [
            'https://i.pinimg.com/736x/0b/e5/a4/0be5a41fc175a65dc0b4239743beca82.jpg',
            'https://i.pinimg.com/736x/7e/49/70/7e4970a27bf538cff4e37604b5c87124.jpg',
            'https://i.pinimg.com/736x/58/2d/c4/582dc4bcf7222205812391e8d7ce3cfd.jpg'
        ],
        'alt': 'Cooking'
    },
    {
        'name': 'Travel',
        'images': [
            'https://i.pinimg.com/736x/e0/17/e6/e017e6c434262a5a19912800235c906a.jpg',
            'https://i.pinimg.com/736x/79/f5/b7/79f5b7b789b3b50786e393c07927f81b.jpg',
            'https://i.pinimg.com/736x/95/ce/be/95cebe0d6432588b9efcb414f47c6094.jpg'
        ],
        'alt': 'Travel'
    }
]

EXPERIENCES = [
    {
        'title': 'Radio Frequency Test Engineer',
        'company': 'Underwriters Laboratories',
        'date': 'April 2024 - August 2024',
        'image': './static/img/ul-logo.png',
        'alt': 'Underwriters Laboratories',
        'description': [
            'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.',
            'Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum. Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium.'
        ],
        'reverse': False
    },
    {
        'title': 'Software Engineering Intern',
        'company': 'UNIPORT',
        'date': 'January 2025 - April 2025',
        'image': './static/img/uniport-logo.png',
        'alt': 'UNIPORT',
        'description': [
            'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.',
            'Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum. Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium.'
        ],
        'reverse': True
    }
]

EDUCATION = {
    'school_name': 'Minerva University',
    'degree': 'Bachelor\'s Degree in Computer Science',
    'date': '2023 - Present',
    'badge_image': '/static/img/mu-image.png',
    'description': 'I am currently enrolled at Minerva University pursuing a Bachelor\'s degree in Computer Science. The program focuses on innovative learning approaches and global perspectives in technology education.'
}

load_dotenv(dotenv_path='../example.env')
app = Flask(__name__)

if os.environ.get("TESTING") == "true":
    print("Running in test mode")
    mydb = SqliteDatabase('file:memory?mode=memory&cache=shared', uri=True)
else:
    mydb = MySQLDatabase(
        os.getenv("MYSQL_DATABASE"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        host=os.getenv("MYSQL_HOST"),
        port=3306
        )


class TimelinePost(Model):
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)
    
    class Meta:
        database = mydb

#mydb.connect()
#mydb.create_tables([TimelinePost])

@app.route('/')
def index():
    return render_template('index.html', title="MLH Fellow", url=os.getenv("URL"))

@app.route('/about')
def about():
    return render_template('about.html', title="About Me - Ekene Azubuko", url=os.getenv("URL"))

@app.route('/hobbies')
def hobbies():
    return render_template('hobbies.html', title="Hobbies - Ekene Azubuko", url=os.getenv("URL"), hobbies=HOBBIES)

@app.route('/experience')
def experience():
    return render_template('experience.html', title="Experience & Education - Ekene Azubuko", url=os.getenv("URL"), experiences=EXPERIENCES)

@app.route('/education')
def education():
    return render_template('education.html', title="Education - Ekene Azubuko", url=os.getenv("URL"), education=EDUCATION)

@app.route('/map')
def map():
    return render_template('map.html', title="Travel Map - Ekene Azubuko", url=os.getenv("URL"))
@app.route('/timeline')
def timeline():
    return render_template('timeline.html', title="Timeline - Ekene Azubuko", url=os.getenv("URL"))

# Name and Email Regex to better handle user inputs with validation
NAME_REGEX = re.compile(r'^[a-zA-Z\s\'\-\.]+$') # letters, spaces, apostrophes, hyphens, dots
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')

@app.route('/api/timeline_post', methods=['POST'])
def post_time_line_post():
    try:
        name = request.form['name']
        email = request.form['email']
        content = request.form['content']
        
        # get all the errors
        errors = []
        if not name:
            errors.append("Name is required")
        elif len(name) < 2:
            errors.append("Name must be at least 2 characters long")
        elif len(name) > 50:
            errors.append("Name must be less than 50 characters")
        elif not NAME_REGEX.match(name):
            errors.append("Name can only contain letters, spaces, apostrophe, hyphens, and dots")
        
        if not email:
            errors.append("Email is required")
        elif not EMAIL_REGEX.match(email):
            errors.append("Please enter a valid email")
        elif len(email) > 100:
            errors.append("Email must be less than 100 characters")
        
        # validate content
        if not content.strip():
            errors.append("Content is required")
        elif len(content) < 1:
            errors.append("Content cannot be empty")
        

        if errors:
            return jsonify({
                'succes': False,
                'error': '; '.join(errors)
            }), 400
        

        timeline_post = TimelinePost.create(name=name, email=email, content=content)
        return model_to_dict(timeline_post)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/timeline_post', methods=['GET'])
def get_time_line_post():
    try:
        return {
            'timeline_posts' : [
                model_to_dict(p)
                for p in 
                TimelinePost.select().order_by(TimelinePost.created_at.desc())
            ]
        }
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/timeline_post/<id>', methods=['DELETE'])
def delete_time_line_post(id):
    try:
        post = TimelinePost.get(TimelinePost.id == id)
        deleted_post = model_to_dict(post)
        post.delete_instance()
        return deleted_post
    except TimelinePost.DoesNotExist:
        return jsonify({'success': False, 'error': 'Post not found'}), 404
