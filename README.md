# Python Challenge - Chat Application

This project uses Django as a backend framework, also uses channels for realtime chat behavior. See the installation instructions and the run settings. 

## Installation

```bash
1. Install redis server from https://redis.io/
2. Enable the service
    sudo service redis-server restart
```
Create a virtual environment.
```python
venv challenge_env
source challenge_env/bin/activate
cd chat
# Use the package manager pip for install requirements
pip install -r requirements.txt

```

## Run Settings
Make sure that redis is running on the default port.

```bash
1. Install redis server from https://redis.io/
2. Enable the service
    sudo service redis-server restart
3. With the virtual environment active:
    python manage.py runserver
```
## How to use

```bash
1. Go to http://localhost:8000
2. Login
    users: chat_user_1 or chat_user_2
    pass: chat_test123
3. Select or create a chat room
4. For new users go to http://localhost:8000/admin/ and click over +Add in Users
```
## Run tests
For running test, make sure that the virtual environment is active
```python
python manage.py test

```
