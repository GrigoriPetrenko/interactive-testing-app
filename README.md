# Interactive Testing Application

A Python-based testing application that reads questions from JSON files and administers interactive tests to users. Available in both **command-line** and **web interface** versions.

## Features

### Core Features
- **Multiple Question Types**: Support for multiple choice, true/false, fill-in-the-blank, and short answer questions
- **Dual Interface**: Both command-line and modern web interface
- **Scoring System**: Points-based scoring with detailed feedback
- **Question Randomization**: Option to randomize question order
- **Results Export**: Save test results to JSON files
- **Category Support**: Organize questions by categories
- **Immediate Feedback**: Instant feedback on answers with explanations

### Web Interface Features
- **Modern UI**: Bootstrap-based responsive design
- **Interactive Testing**: Smooth question navigation with progress tracking
- **Real-time Feedback**: Immediate scoring and explanations
- **File Upload**: Easy question file loading with drag-and-drop
- **Results Visualization**: Charts and detailed result breakdowns
- **Session Management**: Persistent test sessions
- **Mobile Friendly**: Works on all devices

## Requirements

### Command-Line Version
- Python 3.6 or higher
- No external dependencies (uses only standard library)

### Web Interface Version
- Python 3.6 or higher
- Flask 2.0.0 or higher
- Werkzeug 2.0.0 or higher

## Installation

### Quick Start (Web Interface - Recommended)
```bash
# Install dependencies
pip install -r requirements.txt

# Start the web application
python start_web.py
```

The web interface will automatically open in your browser at `http://localhost:5000`

### Command-Line Version
```bash
# No installation required - uses only standard library
python test_app.py
```

## Usage

### Web Interface (Recommended)

1. **Start the application:**
   ```bash
   python start_web.py
   ```

2. **Open your browser** to `http://localhost:5000`

3. **Load questions** by uploading a JSON file or use the sample questions

4. **Take the test** with the interactive web interface

5. **View results** with detailed analytics and export options

### Command-Line Interface

```bash
# Run the application
python test_app.py

# Or run with a questions file directly
python test_app.py sample_questions.json

# Run quick demo
python demo.py

# Run quick test (5 random questions)
python quick_test.py
```

### Question File Format

The application reads questions from JSON files with the following structure:

```json
{
  "title": "Test Title",
  "description": "Test Description",
  "version": "1.0",
  "questions": [
    {
      "id": "unique_question_id",
      "question": "Your question text here?",
      "type": "multiple_choice",
      "options": ["Option 1", "Option 2", "Option 3", "Option 4"],
      "correct_answer": "Option 1",
      "explanation": "Explanation of the correct answer",
      "points": 1,
      "category": "Category Name"
    }
  ]
}
```

### Question Types

1. **Multiple Choice** (`type: "multiple_choice"`)
   - Requires `options` array
   - User selects by number (1, 2, 3, etc.)

2. **True/False** (`type: "true_false"`)
   - User enters true/false
   - Accepts various formats: true, false, t, f, yes, no, y, n, 1, 0

3. **Fill in the Blank** (`type: "fill_blank"`)
   - User types the missing word/phrase
   - Case-insensitive matching

4. **Short Answer** (`type: "short_answer"`)
   - User types a short answer
   - Case-insensitive matching
   - Good for definitions, names, etc.

### Application Menu

When you run the application, you'll see a menu with the following options:

1. **Load questions from file** - Load a new questions file
2. **Show question summary** - Display statistics about loaded questions
3. **Start test (in order)** - Take the test with questions in file order
4. **Start test (randomized)** - Take the test with randomized question order
5. **Exit** - Quit the application

### Test Session

During a test session:

- Questions are displayed one at a time
- You can quit anytime by typing 'quit', 'exit', or 'q'
- Immediate feedback is shown after each answer
- Final score and detailed results are displayed
- Results can be saved to a JSON file

### Sample Questions

The `sample_questions.json` file contains 15 sample questions covering various topics:
- Geography
- Programming
- Astronomy
- Physics
- Mathematics
- History
- Literature
- Computer Science
- Biology
- Chemistry

## Creating Your Own Question Files

1. Create a JSON file following the format shown above
2. Add your questions with appropriate metadata
3. Use the application to load and test your questions

### Tips for Creating Good Questions

- **Clear and unambiguous**: Make sure questions are easy to understand
- **Appropriate difficulty**: Match question difficulty to your audience
- **Good explanations**: Provide helpful explanations for learning
- **Consistent formatting**: Use consistent formatting for options and answers
- **Meaningful categories**: Use categories to organize related questions

## Results File Format

Test results are saved in JSON format with the following structure:

```json
{
  "total_points": 15,
  "max_points": 20,
  "percentage": 75.0,
  "duration": "0:05:32",
  "timestamp": "2024-01-15T10:30:45.123456",
  "results": [
    {
      "question_id": "q1",
      "question": "Question text",
      "user_answer": "User's answer",
      "correct_answer": "Correct answer",
      "is_correct": true,
      "points_earned": 1,
      "max_points": 1,
      "explanation": "Explanation text"
    }
  ]
}
```

## Keyboard Shortcuts

- **Ctrl+C**: Interrupt current operation and return to menu
- **quit/exit/q**: Exit current test session

## Troubleshooting

### Common Issues

1. **File not found**: Make sure the questions file path is correct
2. **Invalid JSON**: Check that your JSON file is properly formatted
3. **No questions loaded**: Verify that your JSON file contains a "questions" array

### Getting Help

If you encounter issues:
1. Check that your JSON file is valid using an online JSON validator
2. Ensure all required fields are present in your questions
3. Verify file permissions allow reading the questions file

## License

This project is open source and available under the MIT License.

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve this application.
