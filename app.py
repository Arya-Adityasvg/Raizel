from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_socketio import SocketIO, emit
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from voice_chatbot import Raizel
import pandas as pd
import json
import os
import base64
import tempfile
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import speech_recognition as sr

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'default_secret_key')
socketio = SocketIO(app, cors_allowed_origins="*")

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# User class for Flask-Login
class User(UserMixin):
    def __init__(self, id, registration_number):
        self.id = id
        self.registration_number = registration_number

# User loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    try:
        student_data = pd.read_csv('Students_Academic_Records.csv')
        student = student_data[student_data['Registration_Number'] == user_id]
        if not student.empty:
            return User(
                id=student.iloc[0]['Registration_Number'],
                registration_number=student.iloc[0]['Registration_Number']
            )
        return None
    except Exception as e:
        print(f"Error loading user: {str(e)}")
        return None

# Initialize the chatbot
raizel = Raizel()

# Load student data
def load_student_data():
    try:
        student_data = pd.read_csv('Students_Academic_Records.csv')
        return student_data
    except Exception as e:
        print(f"Error loading student data: {str(e)}")
        return None

# Load tasks data
def load_tasks_data():
    try:
        tasks_data = pd.read_csv('Academic_Calendar.csv')
        return tasks_data
    except Exception as e:
        print(f"Error loading tasks data: {str(e)}")
        return None

# Load marks data
def load_marks_data():
    try:
        marks_data = pd.read_csv('SubjectWise_Marks.csv')
        return marks_data
    except Exception as e:
        print(f"Error loading marks data: {str(e)}")
        return None

# Load course details
def load_course_details():
    try:
        course_data = pd.read_csv('Student_Course_Details.csv')
        return course_data
    except Exception as e:
        print(f"Error loading course data: {str(e)}")
        return None

# Routes
@app.route('/')
def index():
    if current_user.is_authenticated:
        try:
            # Load data for the current user
            student_data = load_student_data()
            tasks_data = load_tasks_data()
            marks_data = load_marks_data()
            course_data = load_course_details()
            
            # Get student profile
            student_profile = student_data[student_data['Registration_Number'] == current_user.registration_number].iloc[0]
            
            # Get upcoming tasks (next 5)
            upcoming_tasks = tasks_data.head(5).to_dict('records')
            
            # Get academic data (marks)
            academic_data = []
            if marks_data is not None:
                student_marks = marks_data[marks_data['Registration_Number'] == current_user.registration_number]
                if not student_marks.empty:
                    # Get the latest semester's marks
                    latest_semester = student_marks['Semester'].max()
                    latest_marks = student_marks[student_marks['Semester'] == latest_semester]
                    
                    for _, row in latest_marks.iterrows():
                        academic_data.append({
                            'name': row['Subject'],
                            'grade': row['Marks'],
                            'status': 'Pass' if row['Marks'] >= 60 else 'Fail'
                        })
            
            # Get course details
            course_details = []
            if course_data is not None:
                student_courses = course_data[course_data['Registration_Number'] == current_user.registration_number]
                if not student_courses.empty:
                    for _, row in student_courses.iterrows():
                        course_details.append({
                            'department': row['Department'],
                            'enrollment_year': row['Enrollment_Year'],
                            'expected_graduation': row['Expected_Graduation']
                        })
            
            return render_template('index.html', 
                                  user=student_profile['Name'],
                                  academic_data=academic_data,
                                  tasks=upcoming_tasks,
                                  course_details=course_details)
        except Exception as e:
            print(f"Error loading dashboard data: {str(e)}")
            flash(f"Error loading dashboard data: {str(e)}")
            return render_template('index.html', 
                                  user=current_user.registration_number,
                                  academic_data=[],
                                  tasks=[],
                                  course_details=[])
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        registration_number = request.form.get('registration_number')
        
        try:
            student_data = load_student_data()
            if student_data is None:
                flash('Error loading student data. Please try again later.')
                return redirect(url_for('login'))
            
            student = student_data[student_data['Registration_Number'] == registration_number]
            if student.empty:
                flash('Invalid registration number.')
                return redirect(url_for('login'))
            
            user = User(
                id=student.iloc[0]['Registration_Number'],
                registration_number=student.iloc[0]['Registration_Number']
            )
            login_user(user)
            return redirect(url_for('index'))
            
        except Exception as e:
            print(f"Login error: {str(e)}")
            flash('An error occurred. Please try again later.')
            return redirect(url_for('login'))
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/api/chat', methods=['POST'])
@login_required
def chat():
    data = request.json
    message = data.get('message', '')
    
    # Get response from chatbot
    response = raizel.get_response(message)
    
    # If the response contains data-related keywords, fetch and format the data
    if any(keyword in message.lower() for keyword in ['marks', 'grades', 'performance', 'courses', 'subjects']):
        marks_data = load_marks_data()
        course_data = load_course_details()
        
        if marks_data is not None and course_data is not None:
            student_marks = marks_data[marks_data['Registration_Number'] == current_user.registration_number]
            student_courses = course_data[course_data['Registration_Number'] == current_user.registration_number]
            
            if not student_marks.empty:
                marks_info = student_marks.to_dict('records')
                response += f"\n\nYour marks:\n{json.dumps(marks_info, indent=2)}"
            
            if not student_courses.empty:
                courses_info = student_courses.to_dict('records')
                response += f"\n\nYour courses:\n{json.dumps(courses_info, indent=2)}"
    
    return jsonify({'response': response})

@app.route('/api/dashboard')
@login_required
def get_dashboard_data():
    try:
        print(f"Loading dashboard data for user: {current_user.registration_number}")
        
        # Load all required data
        student_data = load_student_data()
        tasks_data = load_tasks_data()
        marks_data = load_marks_data()
        course_data = load_course_details()
        
        # Check if data was loaded successfully
        if student_data is None:
            print("Error: Failed to load student data")
            return jsonify({'error': 'Failed to load student data'})
            
        if tasks_data is None:
            print("Error: Failed to load tasks data")
            return jsonify({'error': 'Failed to load tasks data'})
        
        # Get student profile for the current user
        student_profile = student_data[student_data['Registration_Number'] == current_user.registration_number]
        
        if student_profile.empty:
            print(f"Error: No profile found for user {current_user.registration_number}")
            return jsonify({'error': 'User profile not found'})
            
        student_profile = student_profile.iloc[0].to_dict()
        print(f"Found student profile: {student_profile['Name']}")
        
        # Get upcoming tasks
        upcoming_tasks = tasks_data.head(5).to_dict('records')
        print(f"Loaded {len(upcoming_tasks)} upcoming tasks")
        
        # Get marks and courses
        student_marks = []
        student_courses = []
        
        if marks_data is not None:
            student_marks = marks_data[marks_data['Registration_Number'] == current_user.registration_number].to_dict('records')
            print(f"Loaded {len(student_marks)} marks records")
        
        if course_data is not None:
            student_courses = course_data[course_data['Registration_Number'] == current_user.registration_number].to_dict('records')
            print(f"Loaded {len(student_courses)} course records")
        
        # Get skills and projects (assuming these are in the student profile)
        skills = student_profile.get('Skills', '').split(',') if 'Skills' in student_profile else []
        projects = student_profile.get('Projects', '').split(',') if 'Projects' in student_profile else []
        
        response_data = {
            'profile': {
                'name': student_profile.get('Name', ''),
                'registration_number': student_profile.get('Registration_Number', ''),
                'email': student_profile.get('Email', ''),
                'skills': skills,
                'projects': projects
            },
            'upcoming_tasks': upcoming_tasks,
            'marks': student_marks,
            'courses': student_courses
        }
        
        print("Dashboard data prepared successfully")
        return jsonify(response_data)
        
    except Exception as e:
        print(f"Error in get_dashboard_data: {str(e)}")
        return jsonify({'error': f'Server error: {str(e)}'})

@socketio.on('connect')
def handle_connect():
    print(f"Client connected: {request.sid}")

@socketio.on('disconnect')
def handle_disconnect():
    print(f"Client disconnected: {request.sid}")

@socketio.on('message')
def handle_message(data):
    print(f"Received message: {data}")
    message = data.get('message', '')
    
    # Get response from chatbot
    response = raizel.get_response(message)
    
    # Check for specific keywords to provide more detailed responses
    message_lower = message.lower()
    
    # Handle academic performance queries
    if any(keyword in message_lower for keyword in ['marks', 'grades', 'performance', 'score', 'result']):
        marks_data = load_marks_data()
        
        if marks_data is not None:
            student_marks = marks_data[marks_data['Registration_Number'] == current_user.registration_number]
            
            if not student_marks.empty:
                # Get the latest semester's marks
                latest_semester = student_marks['Semester'].max()
                latest_marks = student_marks[student_marks['Semester'] == latest_semester]
                
                response = f"Here are your marks for semester {latest_semester}:\n\n"
                for _, row in latest_marks.iterrows():
                    status = "Pass" if row['Marks'] >= 60 else "Fail"
                    response += f"- {row['Subject']}: {row['Marks']} ({status})\n"
                
                # Calculate average
                avg_marks = latest_marks['Marks'].mean()
                response += f"\nYour average marks: {avg_marks:.2f}"
            else:
                response = "I couldn't find any marks data for you."
    
    # Handle course queries
    elif any(keyword in message_lower for keyword in ['courses', 'subjects', 'classes', 'department']):
        course_data = load_course_details()
        
        if course_data is not None:
            student_courses = course_data[course_data['Registration_Number'] == current_user.registration_number]
            
            if not student_courses.empty:
                course_info = student_courses.iloc[0]
                response = f"Here are your course details:\n\n"
                response += f"- Department: {course_info['Department']}\n"
                response += f"- Enrollment Year: {course_info['Enrollment_Year']}\n"
                response += f"- Expected Graduation: {course_info['Expected_Graduation']}\n"
            else:
                response = "I couldn't find any course data for you."
    
    # Handle upcoming tasks queries
    elif any(keyword in message_lower for keyword in ['tasks', 'assignments', 'deadlines', 'upcoming', 'schedule']):
        tasks_data = load_tasks_data()
        
        if tasks_data is not None:
            upcoming_tasks = tasks_data.head(5).to_dict('records')
            
            if upcoming_tasks:
                response = "Here are your upcoming tasks:\n\n"
                for task in upcoming_tasks:
                    response += f"- {task['Event_Name']} (Due: {task['Date']})\n"
                    if task['Description']:
                        response += f"  Description: {task['Description']}\n"
            else:
                response = "I couldn't find any upcoming tasks."
    
    # Handle profile queries
    elif any(keyword in message_lower for keyword in ['profile', 'info', 'details', 'about me', 'who am i']):
        student_data = load_student_data()
        
        if student_data is not None:
            student_profile = student_data[student_data['Registration_Number'] == current_user.registration_number]
            
            if not student_profile.empty:
                profile = student_profile.iloc[0]
                response = f"Here are your profile details:\n\n"
                response += f"- Name: {profile['Name']}\n"
                response += f"- Registration Number: {profile['Registration_Number']}\n"
                response += f"- Department: {profile['Department']}\n"
                response += f"- Year: {profile['Year']}\n"
                response += f"- CGPA: {profile['CGPA']}\n"
            else:
                response = "I couldn't find your profile details."
    
    # Emit the response back to the client
    emit('response', {'message': response})

@socketio.on('voice_message')
def handle_voice_message(data):
    try:
        print("Received voice message request")
        
        # Check if this is a text message instead of audio
        if 'message' in data:
            print(f"Received text message: {data['message']}")
            response = raizel.get_response(data['message'])
            emit('voice_response', {'response': response})
            return
            
        # Get the audio data from the client
        audio_data = data.get('audio')
        if not audio_data:
            print("Error: No audio data received")
            emit('voice_response', {'error': 'No audio data received'})
            return
            
        # Process the audio data using speech recognition
        try:
            # Convert base64 audio to audio data
            audio_bytes = base64.b64decode(audio_data.split(',')[1])
            
            # Save to temporary file
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_audio:
                temp_audio.write(audio_bytes)
                temp_audio_path = temp_audio.name
            
            # Initialize recognizer
            recognizer = sr.Recognizer()
            
            # Read the audio file
            with sr.AudioFile(temp_audio_path) as source:
                # Adjust for ambient noise
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                # Record the audio
                audio = recognizer.record(source)
            
            # Clean up temporary file
            os.unlink(temp_audio_path)
            
            # Perform speech recognition
            try:
                # Use Google's speech recognition (faster than other options)
                text = recognizer.recognize_google(audio)
                print(f"Recognized text: {text}")
                
                # Get response from chatbot
                response = raizel.get_response(text)
                
                # Check for specific keywords to provide more detailed responses
                text_lower = text.lower()
                
                # Handle academic performance queries
                if any(keyword in text_lower for keyword in ['marks', 'grades', 'performance', 'score', 'result']):
                    marks_data = load_marks_data()
                    if marks_data is not None:
                        student_marks = marks_data[marks_data['Registration_Number'] == current_user.registration_number]
                        if not student_marks.empty:
                            latest_semester = student_marks['Semester'].max()
                            latest_marks = student_marks[student_marks['Semester'] == latest_semester]
                            response = f"Here are your marks for semester {latest_semester}:\n\n"
                            for _, row in latest_marks.iterrows():
                                status = "Pass" if row['Marks'] >= 60 else "Fail"
                                response += f"- {row['Subject']}: {row['Marks']} ({status})\n"
                            avg_marks = latest_marks['Marks'].mean()
                            response += f"\nYour average marks: {avg_marks:.2f}"
                
                # Handle course queries
                elif any(keyword in text_lower for keyword in ['courses', 'subjects', 'classes', 'department']):
                    course_data = load_course_details()
                    if course_data is not None:
                        student_courses = course_data[course_data['Registration_Number'] == current_user.registration_number]
                        if not student_courses.empty:
                            course_info = student_courses.iloc[0]
                            response = f"Here are your course details:\n\n"
                            response += f"- Department: {course_info['Department']}\n"
                            response += f"- Enrollment Year: {course_info['Enrollment_Year']}\n"
                            response += f"- Expected Graduation: {course_info['Expected_Graduation']}\n"
                
                # Handle upcoming tasks queries
                elif any(keyword in text_lower for keyword in ['tasks', 'assignments', 'deadlines', 'upcoming', 'schedule']):
                    tasks_data = load_tasks_data()
                    if tasks_data is not None:
                        upcoming_tasks = tasks_data.head(5).to_dict('records')
                        if upcoming_tasks:
                            response = "Here are your upcoming tasks:\n\n"
                            for task in upcoming_tasks:
                                response += f"- {task['Event_Name']} (Due: {task['Date']})\n"
                                if task['Description']:
                                    response += f"  Description: {task['Description']}\n"
                
                emit('voice_response', {'response': response})
                
            except sr.UnknownValueError:
                print("Speech recognition could not understand audio")
                emit('voice_response', {'error': "I couldn't understand what you said. Please try again."})
            except sr.RequestError as e:
                print(f"Could not request results from speech recognition service: {e}")
                emit('voice_response', {'error': "There was an error with the speech recognition service. Please try again."})
                
        except Exception as e:
            print(f"Error processing audio: {str(e)}")
            emit('voice_response', {'error': f"Error processing audio: {str(e)}"})
            
    except Exception as e:
        print(f"Error in handle_voice_message: {str(e)}")
        emit('voice_response', {'error': f'Server error: {str(e)}'})

if __name__ == '__main__':
    print("Starting Flask application...")
    print("Starting server on http://127.0.0.1:3000")
    socketio.run(app, host='127.0.0.1', port=3000, debug=True) 