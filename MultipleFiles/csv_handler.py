import csv
import os

def save_user_response(name, age, goal, question, response):
    file_exists = os.path.isfile('user_responses.csv')
    
    with open('user_responses.csv', 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(['Name', 'Age', 'Goal', 'Question', 'Response'])
        writer.writerow([name, age, goal, question, response])
