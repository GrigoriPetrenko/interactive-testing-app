#!/usr/bin/env python3
"""
Interactive Testing Application
Reads questions from JSON files and administers tests to users.
"""

import json
import random
import os
import sys
from typing import List, Dict, Any, Tuple
from datetime import datetime


class Question:
    """Represents a single question with its answers and metadata."""
    
    def __init__(self, data: Dict[str, Any]):
        self.id = data.get('id', '')
        self.question = data.get('question', '')
        self.type = data.get('type', 'multiple_choice')  # multiple_choice, true_false, fill_blank, short_answer
        self.options = data.get('options', [])  # For multiple choice
        self.correct_answer = data.get('correct_answer', '')
        self.explanation = data.get('explanation', '')
        self.points = data.get('points', 1)
        self.category = data.get('category', 'General')
    
    def display(self, show_answer: bool = False) -> str:
        """Display the question in a formatted way."""
        output = f"\n{self.question}\n"
        output += f"Category: {self.category} | Points: {self.points}\n"
        output += "-" * 50 + "\n"
        
        if self.type == 'multiple_choice':
            for i, option in enumerate(self.options, 1):
                marker = "✓" if show_answer and option == self.correct_answer else " "
                output += f"{marker} {i}. {option}\n"
        
        elif self.type == 'true_false':
            options = ['True', 'False']
            for i, option in enumerate(options, 1):
                marker = "✓" if show_answer and option == self.correct_answer else " "
                output += f"{marker} {i}. {option}\n"
        
        elif self.type in ['fill_blank', 'short_answer']:
            if show_answer:
                output += f"Correct answer: {self.correct_answer}\n"
        
        return output
    
    def check_answer(self, user_answer: str) -> Tuple[bool, float]:
        """Check if the user's answer is correct and return score."""
        if self.type == 'multiple_choice':
            try:
                choice_index = int(user_answer) - 1
                if 0 <= choice_index < len(self.options):
                    selected = self.options[choice_index]
                    return selected == self.correct_answer, self.points if selected == self.correct_answer else 0
            except ValueError:
                return False, 0
        
        elif self.type == 'true_false':
            answer_bool = user_answer.lower().strip() in ['true', 't', '1', 'yes', 'y']
            correct_bool = self.correct_answer.lower().strip() in ['true', 't', '1', 'yes', 'y']
            return answer_bool == correct_bool, self.points if answer_bool == correct_bool else 0
        
        elif self.type in ['fill_blank', 'short_answer']:
            # Case-insensitive comparison for text answers
            user_clean = user_answer.lower().strip()
            correct_clean = self.correct_answer.lower().strip()
            return user_clean == correct_clean, self.points if user_clean == correct_clean else 0
        
        return False, 0


class TestSession:
    """Manages a test session with questions and scoring."""
    
    def __init__(self, questions: List[Question]):
        self.questions = questions
        self.results = []
        self.start_time = None
        self.end_time = None
        self.current_question_index = 0
    
    def start_test(self):
        """Start the test session."""
        self.start_time = datetime.now()
        print(f"\n{'='*60}")
        print(f"TEST SESSION STARTED")
        print(f"Total Questions: {len(self.questions)}")
        print(f"Total Points Available: {sum(q.points for q in self.questions)}")
        print(f"{'='*60}")
    
    def get_current_question(self) -> Question:
        """Get the current question."""
        return self.questions[self.current_question_index]
    
    def submit_answer(self, answer: str) -> bool:
        """Submit an answer and move to next question."""
        question = self.get_current_question()
        is_correct, points = question.check_answer(answer)
        
        result = {
            'question_id': question.id,
            'question': question.question,
            'user_answer': answer,
            'correct_answer': question.correct_answer,
            'is_correct': is_correct,
            'points_earned': points,
            'max_points': question.points,
            'explanation': question.explanation
        }
        
        self.results.append(result)
        
        # Show immediate feedback
        print(f"\n{'✓ CORRECT!' if is_correct else '✗ INCORRECT!'}")
        if question.explanation:
            print(f"Explanation: {question.explanation}")
        
        self.current_question_index += 1
        return self.current_question_index < len(self.questions)
    
    def finish_test(self):
        """Finish the test session and calculate final score."""
        self.end_time = datetime.now()
        total_points = sum(r['points_earned'] for r in self.results)
        max_points = sum(r['max_points'] for r in self.results)
        percentage = (total_points / max_points * 100) if max_points > 0 else 0
        
        print(f"\n{'='*60}")
        print(f"TEST COMPLETED!")
        print(f"Score: {total_points}/{max_points} ({percentage:.1f}%)")
        print(f"Duration: {self.end_time - self.start_time}")
        print(f"{'='*60}")
        
        return {
            'total_points': total_points,
            'max_points': max_points,
            'percentage': percentage,
            'duration': self.end_time - self.start_time,
            'results': self.results
        }
    
    def show_detailed_results(self):
        """Show detailed results for each question."""
        print(f"\n{'='*60}")
        print("DETAILED RESULTS")
        print(f"{'='*60}")
        
        for i, result in enumerate(self.results, 1):
            question = self.questions[i-1]
            print(f"\nQuestion {i}: {question.question}")
            print(f"Your answer: {result['user_answer']}")
            print(f"Correct answer: {result['correct_answer']}")
            print(f"Result: {'✓ CORRECT' if result['is_correct'] else '✗ INCORRECT'}")
            print(f"Points: {result['points_earned']}/{result['max_points']}")
            if result['explanation']:
                print(f"Explanation: {result['explanation']}")
            print("-" * 40)


class TestApp:
    """Main application class."""
    
    def __init__(self):
        self.questions = []
        self.test_session = None
    
    def load_questions(self, filename: str) -> bool:
        """Load questions from a JSON file."""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.questions = [Question(q) for q in data.get('questions', [])]
            print(f"Loaded {len(self.questions)} questions from {filename}")
            return True
        
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
            return False
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON in '{filename}': {e}")
            return False
        except Exception as e:
            print(f"Error loading questions: {e}")
            return False
    
    def show_question_summary(self):
        """Show a summary of loaded questions."""
        if not self.questions:
            print("No questions loaded.")
            return
        
        categories = {}
        total_points = 0
        
        for q in self.questions:
            category = q.category
            if category not in categories:
                categories[category] = {'count': 0, 'points': 0}
            categories[category]['count'] += 1
            categories[category]['points'] += q.points
            total_points += q.points
        
        print(f"\n{'='*60}")
        print("QUESTION SUMMARY")
        print(f"{'='*60}")
        print(f"Total Questions: {len(self.questions)}")
        print(f"Total Points: {total_points}")
        print("\nBy Category:")
        
        for category, info in categories.items():
            print(f"  {category}: {info['count']} questions ({info['points']} points)")
        
        print(f"{'='*60}")
    
    def start_interactive_test(self, randomize: bool = False):
        """Start an interactive test session."""
        if not self.questions:
            print("No questions loaded. Please load a questions file first.")
            return
        
        questions_to_use = self.questions.copy()
        if randomize:
            random.shuffle(questions_to_use)
            print("Questions randomized!")
        
        self.test_session = TestSession(questions_to_use)
        self.test_session.start_test()
        
        while self.test_session.current_question_index < len(self.test_session.questions):
            question = self.test_session.get_current_question()
            progress = f"({self.test_session.current_question_index + 1}/{len(self.test_session.questions)})"
            
            print(f"\n{progress} {question.display()}")
            
            if question.type == 'multiple_choice':
                print("Enter your choice (1, 2, 3, etc.): ", end="")
            elif question.type == 'true_false':
                print("Enter your answer (true/false): ", end="")
            elif question.type in ['fill_blank', 'short_answer']:
                print("Enter your answer: ", end="")
            
            try:
                answer = input().strip()
                if answer.lower() in ['quit', 'exit', 'q']:
                    print("Test cancelled by user.")
                    return
                
                has_more = self.test_session.submit_answer(answer)
                if not has_more:
                    break
            
            except KeyboardInterrupt:
                print("\nTest interrupted by user.")
                return
        
        # Show final results
        final_score = self.test_session.finish_test()
        
        # Ask if user wants detailed results
        try:
            show_details = input("\nShow detailed results? (y/n): ").lower().strip()
            if show_details in ['y', 'yes']:
                self.test_session.show_detailed_results()
        except KeyboardInterrupt:
            pass
        
        # Ask if user wants to save results
        try:
            save_results = input("\nSave results to file? (y/n): ").lower().strip()
            if save_results in ['y', 'yes']:
                self.save_results(final_score)
        except KeyboardInterrupt:
            pass
    
    def save_results(self, results: Dict):
        """Save test results to a file."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"test_results_{timestamp}.json"
        
        try:
            # Convert datetime objects to strings for JSON serialization
            results_copy = results.copy()
            results_copy['duration'] = str(results_copy['duration'])
            results_copy['timestamp'] = datetime.now().isoformat()
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(results_copy, f, indent=2, ensure_ascii=False)
            
            print(f"Results saved to {filename}")
        
        except Exception as e:
            print(f"Error saving results: {e}")
    
    def show_menu(self):
        """Show the main menu."""
        while True:
            print(f"\n{'='*60}")
            print("INTERACTIVE TESTING APPLICATION")
            print(f"{'='*60}")
            print("1. Load questions from file")
            print("2. Show question summary")
            print("3. Start test (in order)")
            print("4. Start test (randomized)")
            print("5. Exit")
            print(f"{'='*60}")
            
            try:
                choice = input("Enter your choice (1-5): ").strip()
                
                if choice == '1':
                    filename = input("Enter questions file path: ").strip()
                    if filename:
                        self.load_questions(filename)
                
                elif choice == '2':
                    self.show_question_summary()
                
                elif choice == '3':
                    self.start_interactive_test(randomize=False)
                
                elif choice == '4':
                    self.start_interactive_test(randomize=True)
                
                elif choice == '5':
                    print("Goodbye!")
                    break
                
                else:
                    print("Invalid choice. Please enter 1-5.")
            
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"An error occurred: {e}")


def main():
    """Main entry point."""
    print("Welcome to the Interactive Testing Application!")
    
    app = TestApp()
    
    # Check if a questions file was provided as command line argument
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        if app.load_questions(filename):
            app.show_question_summary()
            # Ask if user wants to start test immediately
            try:
                start_now = input("\nStart test immediately? (y/n): ").lower().strip()
                if start_now in ['y', 'yes']:
                    randomize = input("Randomize questions? (y/n): ").lower().strip() in ['y', 'yes']
                    app.start_interactive_test(randomize=randomize)
                else:
                    app.show_menu()
            except KeyboardInterrupt:
                print("\nGoodbye!")
        else:
            app.show_menu()
    else:
        app.show_menu()


if __name__ == "__main__":
    main()

