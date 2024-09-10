from flask import Flask, render_template, request
import random

app = Flask(__name__)

import random

def generate_equations(num, max_value):
    equations = set()
    unique_equations = []

    while len(unique_equations) < num:
        num1 = random.randint(1, max_value)
        num2 = random.randint(1, max_value)
        operation = random.choice(['+', '-'])
        
        if operation == '-' and num1 < num2:
            num1, num2 = num2, num1
            
        equation = f"{num1} {operation} {num2}"
        
        if equation not in equations:
            answer = eval(equation)
            equations.add(equation)
            unique_equations.append((equation, answer))
    
    return unique_equations


@app.route('/')
def index():
    num = request.args.get('num', default=20, type=int)  #http://localhost:5000/?max=30
    max_value = request.args.get('max', default=20, type=int) 
    equations = generate_equations(num,max_value)
    return render_template('index.html', equations=equations)

@app.route('/check', methods=['POST'])
def check_answers():
    user_answers = request.form.to_dict()
    equations = [(eq, eval(eq)) for eq in user_answers]
    results = []

    for eq, correct_answer in equations:
        user_answer = user_answers.get(eq, None)
        correct = user_answer is not None and user_answer and int(user_answer) == correct_answer
        results.append((eq, correct_answer, user_answer, correct)) 

    all_correct = all(correct for _, _, _, correct in results)

    return render_template('updated_form.html', results=results, all_correct=all_correct)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
