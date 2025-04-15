from flask import Flask, request, jsonify

app = Flask(__name__)

questions = [
    {"question": "What is 2 + 2?", "difficulty": "easy"},
    {"question": "What is the capital of France?", "difficulty": "hard"},
    {"question": "What is the square root of 64?", "difficulty": "hard"},
    {"question": "Who wrote 'Romeo and Juliet'?", "difficulty": "medium"},
    {"question": "What is the chemical symbol for water?", "difficulty": "hard"}
]

@app.route('/question_count', methods=['GET'])


def get_question_count():
    difficulty_level = request.args.get('difficulty')
    
    if not difficulty_level:
        return jsonify({"error": "Difficulty level parameter is missing"}), 400
    
    filtered_questions = [q for q in questions if q['difficulty'] == difficulty_level]
    
    question_count = len(filtered_questions)
    
    response = {
        "difficulty": difficulty_level,
        "question_count": question_count
    }
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)