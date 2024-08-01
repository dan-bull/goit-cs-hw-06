import socket
import json
from pymongo import MongoClient
import logging

# Налаштування логування
logging.basicConfig(level=logging.DEBUG)

# Підключення до MongoDB
client = MongoClient('mongodb://db:27017/')
db = client['message_db']
collection = db['messages']

def handle_message(data):
    message = json.loads(data)
    logging.debug(f'Received message: {message}')
    # Збереження в MongoDB
    collection.insert_one(message)
    logging.debug(f'Message saved to MongoDB: {message}')

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind(('0.0.0.0', 5000))
        logging.info('Socket server listening on port 5000')
        while True:
            data, addr = s.recvfrom(1024)
            handle_message(data)

if __name__ == "__main__":
    main()
