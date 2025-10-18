#!/usr/bin/env python3
"""
Quick test script for the Interactive Testing Application
This script provides a fast way to test the application with the sample questions.
"""

import sys
import os
from test_app import TestApp

def main():
    """Run a quick test with sample questions."""
    print("Quick Test - Interactive Testing Application")
    print("=" * 50)
    
    # Check if sample questions file exists
    sample_file = "sample_questions.json"
    if not os.path.exists(sample_file):
        print(f"Error: {sample_file} not found!")
        print("Please make sure you're running this from the correct directory.")
        return 1
    
    # Create app and load questions
    app = TestApp()
    if not app.load_questions(sample_file):
        print("Failed to load sample questions!")
        return 1
    
    # Show summary
    app.show_question_summary()
    
    # Ask user what they want to do
    print("\nWhat would you like to do?")
    print("1. Take a quick test (5 random questions)")
    print("2. Take the full test")
    print("3. Exit")
    
    try:
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == "1":
            # Take a quick test with 5 random questions
            import random
            app.questions = random.sample(app.questions, min(5, len(app.questions)))
            print(f"\nTaking quick test with {len(app.questions)} random questions...")
            app.start_interactive_test(randomize=False)
        
        elif choice == "2":
            # Take full test
            randomize = input("Randomize questions? (y/n): ").lower().strip() in ['y', 'yes']
            app.start_interactive_test(randomize=randomize)
        
        elif choice == "3":
            print("Goodbye!")
        
        else:
            print("Invalid choice!")
            return 1
    
    except KeyboardInterrupt:
        print("\nGoodbye!")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

