from flask import Flask, render_template, request
import random

app = Flask(__name__)

# Функция для генерации уравнений
def generate_equations(num=20, max_value=20):
    equations = []
    for _ in range(num):
        num1 = random.randint(1, max_value)
        num2 = random.randint(1, max_value)
        operation = random.choice(['+', '-'])
        if operation == '-':
            if num1 < num2:
                num1, num2 = num2, num1
        equation = f"{num1} {operation} {num2}"
        answer = eval(equation)
        equations.append((equation, answer))
    return equations

@app.route('/')
def index():
    equations = generate_equations()
    return render_template('index.html', equations=equations)

@app.route('/check', methods=['POST'])
def check_answers():
    user_answers = request.form.to_dict()
    equations = [(eq, eval(eq)) for eq in user_answers]  # Получение исходных уравнений и правильных ответов
    results = []

    # Проверка каждого уравнения на правильность
    for eq, correct_answer in equations:
        user_answer = user_answers.get(eq, None)
        correct = user_answer is not None and int(user_answer) == correct_answer
        results.append((eq, correct_answer, user_answer, correct))  # Сохраняем ответ пользователя

    all_correct = all(correct for _, _, _, correct in results)

    # Возвращаем обновлённую форму с результатами и введёнными значениями
    return render_template('updated_form.html', results=results, all_correct=all_correct)

if __name__ == '__main__':
    app.run(debug=True)
