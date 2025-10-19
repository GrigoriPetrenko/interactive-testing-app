# ServiceNow Questions to JSON Conversion Prompt

## Purpose

This prompt is used to convert ServiceNow single and multiple-choice questions into JSON format for easier processing, study, or importing into quiz tools.

## ITSM Categories

These categories are relevant for ITSM questions:

* Incident Management
* Problem Management
* Change Management
* Request Management / Service Catalog
* Knowledge Management
* Configuration Management (CMDB)
* Reports & Dashboards

## JSON Format

```json
{
  "questions": [
    {
      "question": "Your question here?",
      "type": "multiple_choice",
      "options": ["A. ...", "B. ...", "C. ...", "D. ..."],
      "correct_answer": "A",
      "explanation": "Explanation here",
      "points": 1,
      "category": "Category here"
    }
  ],
  "summary": {
    "total_questions_received": 0,
    "total_questions_converted": 0,
    "missing_question_numbers": []
  }
}
```

## Instructions

1. Keep the A./B./C./D. prefixes inside the options.
2. The ✅ symbol indicates the correct answer(s). Remove ✅ from option text.
3. If multiple options have ✅, use an array for correct_answer: `"correct_answer": ["A","D"]`.
4. If an explanation is provided after the question, include it; otherwise leave it blank.
5. If a category can be inferred from the topic, fill it in; otherwise leave it blank.
6. Include all questions exactly as numbered in the input; do not skip any numbers.
7. Verify that question numbers are sequential. If any numbers are missing or duplicated, list them in `missing_question_numbers` in the summary.
8. Each batch should contain up to 10 questions.
9. Include `next_batch_start` in the summary if more questions remain.

## Input Format

Questions will be sent in the following format:

```
1. Question text  
A. Option  
B. Option  
C. Option ✅   <-- ✅ marks the correct answer  
D. Option  
Explanation (if any)
```

## Rules

* The ✅ symbol in the input **indicates the correct answer**.
* In the JSON output, **remove ✅ from the option text**.
* Set the correct answer in the "correct_answer" field. If multiple options have ✅, use an array.
* Ensure every numbered question in the input is added to the JSON.
* If any question numbers are skipped or duplicated, report them in `missing_question_numbers`.

## Final Message

At the end of the JSON, include a summary object showing:

* `total_questions_received`: number of questions in the input
* `total_questions_converted`: number of questions successfully added to JSON
* `missing_question_numbers`: any skipped or duplicated question numbers
* `next_batch_start`: the number of the next question if more remain
