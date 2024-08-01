from flask import Flask, render_template, request, redirect, url_for
import socket
import json
from datetime import datetime
import os
import logging

app = Flask(__name__)

# Налаштування логування
logging.basicConfig(level=logging.DEBUG)

# Шлях до файлу data.json
DATA_FILE_PATH = 'storage/data.json'

def save_message_to_file(message_data):
    if not os.path.exists('storage'):
        os.makedirs('storage')
    if not os.path.exists(DATA_FILE_PATH):
        with open(DATA_FILE_PATH, 'w') as f:
            json.dump({}, f)  # Ініціалізуємо порожній словник
    
    with open(DATA_FILE_PATH, 'r+') as f:
        try:
            data = json.load(f)
            if not isinstance(data, dict):
                logging.warning(f"Invalid data format in {DATA_FILE_PATH}. Initializing empty dictionary.")
                data = {}
        except json.JSONDecodeError:
            logging.error(f"Error decoding JSON from {DATA_FILE_PATH}. Initializing empty dictionqary.")
            data = {}
        
        # Використання часу як унікального ключа
        message_key = str(datetime.now())
        data[message_key] = message_data
        
        f.seek(0)
        json.dump(data, f, indent=4)
    logging.debug(f'Message saved to file: {message_data}')



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/message', methods=['GET', 'POST'])
def message():
    if request.method == 'POST':
        username = request.form['username']
        message_text = request.form['message']
        date = str(datetime.now())
        message_data = {
            "date": date,
            "username": username,
            "message": message_text
        }
        
        # Збереження повідомлення у файл
        save_message_to_file(message_data)
        
        # Відправлення повідомлення на Socket-сервер
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.sendto(json.dumps(message_data).encode(), ('socket_server', 5000))
        logging.debug(f'Message sent to socket server: {message_data}')
        
        return redirect(url_for('index'))
    return render_template('message.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html'), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
