#!/usr/bin/env python3
"""
Web-based Interactive Testing Application
Flask web interface for the testing application.
"""

import json
import random
import os
from datetime import datetime
from flask import Flask, render_template, request, session, redirect, url_for, flash, jsonify
from werkzeug.utils import secure_filename

# Import our existing classes
from test_app import Question, TestSession

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'json'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    """Check if file has allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Home page."""
    return render_template('index.html')

@app.route('/load_questions', methods=['GET', 'POST'])
def load_questions():
    """Load questions from file."""
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file selected')
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            flash('No file selected')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Load questions
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                questions = [Question(q) for q in data.get('questions', [])]
                session['questions'] = [
                    {
                        'id': q.id,
                        'question': q.question,
                        'type': q.type,
                        'options': q.options,
                        'correct_answer': q.correct_answer,
                        'explanation': q.explanation,
                        'points': q.points,
                        'category': q.category
                    } for q in questions
                ]
                
                session['test_title'] = data.get('title', 'Untitled Test')
                session['test_description'] = data.get('description', '')
                
                flash(f'Successfully loaded {len(questions)} questions!')
                return redirect(url_for('question_summary'))
            
            except Exception as e:
                flash(f'Error loading questions: {str(e)}')
                return redirect(request.url)
    
    return render_template('load_questions.html')

@app.route('/question_summary')
def question_summary():
    """Show question summary."""
    questions = session.get('questions', [])
    if not questions:
        flash('No questions loaded. Please load a questions file first.')
        return redirect(url_for('load_questions'))
    
    # Calculate summary statistics
    categories = {}
    total_points = 0
    
    for q in questions:
        category = q['category']
        if category not in categories:
            categories[category] = {'count': 0, 'points': 0}
        categories[category]['count'] += 1
        categories[category]['points'] += q['points']
        total_points += q['points']
    
    return render_template('question_summary.html', 
                         questions=questions,
                         categories=categories,
                         total_points=total_points,
                         test_title=session.get('test_title', 'Untitled Test'))

@app.route('/start_test')
def start_test():
    """Start a new test session."""
    questions = session.get('questions', [])
    if not questions:
        flash('No questions loaded. Please load a questions file first.')
        return redirect(url_for('load_questions'))
    
    # Check for randomization
    randomize = request.args.get('randomize', 'false').lower() == 'true'
    
    if randomize:
        questions = random.sample(questions, len(questions))
    
    # Initialize test session
    session['test_questions'] = questions
    session['current_question'] = 0
    session['test_results'] = []
    session['test_start_time'] = datetime.now().isoformat()
    session['randomized'] = randomize
    
    return redirect(url_for('take_test'))

@app.route('/take_test')
def take_test():
    """Display current question for testing."""
    questions = session.get('test_questions', [])
    current_index = session.get('current_question', 0)
    
    if not questions or current_index >= len(questions):
        return redirect(url_for('test_complete'))
    
    question = questions[current_index]
    progress = current_index + 1
    total = len(questions)
    
    return render_template('take_test.html', 
                         question=question,
                         progress=progress,
                         total=total,
                         current_index=current_index)

@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    """Submit an answer and move to next question."""
    questions = session.get('test_questions', [])
    current_index = session.get('current_question', 0)
    results = session.get('test_results', [])
    
    if current_index >= len(questions):
        return redirect(url_for('test_complete'))
    
    question_data = questions[current_index]
    user_answer = request.form.get('answer', '').strip()
    
    # Create Question object for checking
    question = Question(question_data)
    is_correct, points = question.check_answer(user_answer)
    
    # Get the correct answer text for display
    correct_answer_display = question.correct_answer
    if question.type == 'multiple_choice' and len(question.correct_answer) == 1 and question.correct_answer.isalpha():
        # If correct answer is just a letter, find the corresponding option text
        try:
            letter_index = ord(question.correct_answer.upper()) - ord('A')
            if 0 <= letter_index < len(question.options):
                correct_answer_display = question.options[letter_index]
        except:
            pass  # Keep original if conversion fails
    
    # Get the user answer text for display
    user_answer_display = user_answer
    if question.type == 'multiple_choice' and user_answer.isdigit():
        # Convert user's numeric choice to option text
        try:
            choice_index = int(user_answer) - 1
            if 0 <= choice_index < len(question.options):
                user_answer_display = question.options[choice_index]
        except:
            pass  # Keep original if conversion fails
    
    # Store result
    result = {
        'question_id': question.id,
        'question': question.question,
        'user_answer': user_answer_display,
        'correct_answer': correct_answer_display,
        'is_correct': is_correct,
        'points_earned': points,
        'max_points': question.points,
        'explanation': question.explanation
    }
    
    results.append(result)
    session['test_results'] = results
    session['current_question'] = current_index + 1
    
    return redirect(url_for('take_test'))

@app.route('/test_complete')
def test_complete():
    """Show test completion and results."""
    results = session.get('test_results', [])
    start_time = session.get('test_start_time')
    
    if not results:
        flash('No test results found.')
        return redirect(url_for('index'))
    
    # Calculate final score
    total_points = sum(r['points_earned'] for r in results)
    max_points = sum(r['max_points'] for r in results)
    percentage = (total_points / max_points * 100) if max_points > 0 else 0
    
    # Calculate duration
    duration = "Unknown"
    if start_time:
        try:
            start_dt = datetime.fromisoformat(start_time)
            duration_dt = datetime.now() - start_dt
            duration = str(duration_dt).split('.')[0]  # Remove microseconds
        except:
            pass
    
    return render_template('test_complete.html',
                         results=results,
                         total_points=total_points,
                         max_points=max_points,
                         percentage=percentage,
                         duration=duration)

@app.route('/export_results')
def export_results():
    """Export test results as JSON."""
    results = session.get('test_results', [])
    start_time = session.get('test_start_time')
    
    if not results:
        return jsonify({'error': 'No results to export'}), 400
    
    # Calculate final score
    total_points = sum(r['points_earned'] for r in results)
    max_points = sum(r['max_points'] for r in results)
    percentage = (total_points / max_points * 100) if max_points > 0 else 0
    
    # Prepare export data
    export_data = {
        'test_title': session.get('test_title', 'Untitled Test'),
        'total_points': total_points,
        'max_points': max_points,
        'percentage': percentage,
        'duration': "Unknown",
        'timestamp': datetime.now().isoformat(),
        'randomized': session.get('randomized', False),
        'results': results
    }
    
    # Calculate duration if possible
    if start_time:
        try:
            start_dt = datetime.fromisoformat(start_time)
            duration_dt = datetime.now() - start_dt
            export_data['duration'] = str(duration_dt)
        except:
            pass
    
    # Create filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"test_results_{timestamp}.json"
    
    # Save file
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(export_data, f, indent=2, ensure_ascii=False)
    
    return jsonify({
        'message': f'Results exported to {filename}',
        'filename': filename
    })

@app.route('/api/questions')
def api_questions():
    """API endpoint to get current questions."""
    return jsonify(session.get('questions', []))

@app.route('/api/results')
def api_results():
    """API endpoint to get current test results."""
    return jsonify(session.get('test_results', []))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

