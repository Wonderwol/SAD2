from waitress import serve
from app import app  # Импортируйте ваше приложение Flask

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=5000)  # Запуск на порту 5000
