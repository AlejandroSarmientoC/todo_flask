import pytest
import mongomock
from app.models import User, Task
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId
from flask import Flask
from app import mongo

# Configura una aplicación Flask para pruebas
@pytest.fixture(scope='module')
def app():
    app = Flask(__name__)
    app.config["TESTING"] = True
    app.config["MONGO_URI"] = "mongomock://localhost"
    mongo.db = mongomock.MongoClient().db
    yield app

@pytest.fixture(scope='module')
def client(app):
    return app.test_client()

def test_user_registration(client):
    # Crear un nuevo usuario
    user = User(username='testuser', email='testuser@example.com')
    user.set_password('testpassword')
    user.save()

    # Verificar que el usuario se ha guardado correctamente
    saved_user = User.get_by_username('testuser')
    assert saved_user is not None
    assert saved_user.username == 'testuser'
    assert saved_user.email == 'testuser@example.com'
    assert saved_user.check_password('testpassword')

def test_user_login(client):
    # Crear un nuevo usuario
    user = User(username='loginuser', email='loginuser@example.com')
    user.set_password('loginpassword')
    user.save()

    # Intentar iniciar sesión con las credenciales correctas
    login_user = User.get_by_username('loginuser')
    assert login_user is not None
    assert login_user.check_password('loginpassword')

    # Intentar iniciar sesión con una contraseña incorrecta
    assert not login_user.check_password('wrongpassword')

def test_task_creation(client):
    # Crear un nuevo usuario para asociar la tarea
    user = User(username='taskuser', email='taskuser@example.com')
    user.set_password('taskpassword')
    user.save()
    user_id = user.id

    # Crear una nueva tarea
    task = Task(description='Test task', user_id=user_id)
    task.save()

    # Verificar que la tarea se ha guardado correctamente
    saved_tasks = Task.get_all_by_user(user_id)
    assert len(saved_tasks) == 1
    assert saved_tasks[0].description == 'Test task'
    assert saved_tasks[0].user_id == user_id

def test_task_deletion(client):
    # Crear un nuevo usuario para asociar la tarea
    user = User(username='deleteuser', email='deleteuser@example.com')
    user.set_password('deletepassword')
    user.save()
    user_id = user.id

    # Crear una nueva tarea
    task = Task(description='Task to be deleted', user_id=user_id)
    task.save()
    task_id = task.id

    # Eliminar la tarea
    task.delete()

    # Verificar que la tarea se ha eliminado correctamente
    deleted_task = Task.get(task_id)
    assert deleted_task is None
