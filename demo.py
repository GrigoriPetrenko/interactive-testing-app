#!/usr/bin/env python3
"""
Demo script for the Interactive Testing Application
This script demonstrates how to use the testing application programmatically.
"""

from test_app import TestApp, Question
import json


def create_demo_questions():
    """Create a small set of demo questions."""
    demo_data = {
        "title": "Quick Demo Test",
        "description": "A short demonstration test",
        "version": "1.0",
        "questions": [
            {
                "id": "demo1",
                "question": "What is 2 + 2?",
                "type": "multiple_choice",
                "options": ["3", "4", "5", "6"],
                "correct_answer": "4",
                "explanation": "Basic arithmetic: 2 + 2 = 4",
                "points": 1,
                "category": "Math"
            },
            {
                "id": "demo2",
                "question": "Python is easy to learn.",
                "type": "true_false",
                "correct_answer": "True",
                "explanation": "Python is known for its simple and readable syntax.",
                "points": 1,
                "category": "Programming"
            }
        ]
    }
    
    with open('demo_questions.json', 'w') as f:
        json.dump(demo_data, f, indent=2)
    
    print("Created demo_questions.json with 2 sample questions")


def demonstrate_programmatic_usage():
    """Demonstrate using the TestApp programmatically."""
    print("\n" + "="*60)
    print("DEMONSTRATING PROGRAMMATIC USAGE")
    print("="*60)
    
    # Create demo questions
    create_demo_questions()
    
    # Create app instance
    app = TestApp()
    
    # Load questions
    if app.load_questions('demo_questions.json'):
        app.show_question_summary()
        
        # Create a test session
        from test_app import TestSession
        session = TestSession(app.questions)
        session.start_test()
        
        # Simulate some answers
        print("\nSimulating test answers...")
        
        # Answer first question correctly
        session.submit_answer("2")  # Should be correct (4 is option 2)
        
        # Answer second question correctly  
        session.submit_answer("True")  # Should be correct
        
        # Show results
        results = session.finish_test()
        session.show_detailed_results()
        
        print(f"\nDemo completed! Final score: {results['total_points']}/{results['max_points']}")
    
    # Clean up
    import os
    if os.path.exists('demo_questions.json'):
        os.remove('demo_questions.json')
        print("Cleaned up demo file")


def show_question_examples():
    """Show examples of different question types."""
    print("\n" + "="*60)
    print("QUESTION TYPE EXAMPLES")
    print("="*60)
    
    # Multiple choice example
    mc_data = {
        "id": "example1",
        "question": "What is the capital of Japan?",
        "type": "multiple_choice",
        "options": ["Beijing", "Seoul", "Tokyo", "Bangkok"],
        "correct_answer": "Tokyo",
        "explanation": "Tokyo is the capital and largest city of Japan.",
        "points": 2,
        "category": "Geography"
    }
    
    mc_question = Question(mc_data)
    print("Multiple Choice Question:")
    print(mc_question.display())
    
    # True/False example
    tf_data = {
        "id": "example2",
        "question": "The Earth is flat.",
        "type": "true_false",
        "correct_answer": "False",
        "explanation": "The Earth is approximately spherical (oblate spheroid).",
        "points": 1,
        "category": "Science"
    }
    
    tf_question = Question(tf_data)
    print("\nTrue/False Question:")
    print(tf_question.display())
    
    # Fill in the blank example
    fib_data = {
        "id": "example3",
        "question": "The _____ is the largest organ in the human body.",
        "type": "fill_blank",
        "correct_answer": "skin",
        "explanation": "The skin is indeed the largest organ in the human body.",
        "points": 2,
        "category": "Biology"
    }
    
    fib_question = Question(fib_data)
    print("\nFill in the Blank Question:")
    print(fib_question.display())


def main():
    """Main demo function."""
    print("Interactive Testing Application - Demo")
    print("This demo shows various features of the testing application.\n")
    
    # Show question examples
    show_question_examples()
    
    # Demonstrate programmatic usage
    demonstrate_programmatic_usage()
    
    print("\n" + "="*60)
    print("DEMO COMPLETED")
    print("="*60)
    print("To run the interactive application:")
    print("  python test_app.py")
    print("  python test_app.py sample_questions.json")
    print("\nTo see the full menu:")
    print("  python test_app.py")


if __name__ == "__main__":
    main()

