import pytest
from app import app, tasks

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_index(client):
    """Test the index page"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'My To-Do List' in response.data

def test_add_task(client):
    """Test adding a new task"""
    initial_task_count = len(tasks)
    response = client.post('/add', data={'task': 'Test Task'})
    assert response.status_code == 302  # Redirect after adding task
    assert len(tasks) == initial_task_count + 1
    assert tasks[-1]['task'] == 'Test Task'
    assert tasks[-1]['completed'] is False

def test_complete_task(client):
    """Test completing a task"""
    client.post('/add', data={'task': 'Test Task to Complete'})
    task_id = len(tasks) - 1
    response = client.get(f'/complete/{task_id}')
    assert response.status_code == 302  # Redirect after completing task
    assert tasks[task_id]['completed'] is True
    # Toggle back to not completed
    client.get(f'/complete/{task_id}')
    assert tasks[task_id]['completed'] is False

def test_delete_task(client):
    """Test deleting a task"""
    client.post('/add', data={'task': 'Test Task to Delete'})
    task_id = len(tasks) - 1
    response = client.get(f'/delete/{task_id}')
    assert response.status_code == 302  # Redirect after deleting task
    assert len(tasks) == task_id  # Task count should decrease by 1