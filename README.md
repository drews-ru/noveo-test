# noveo-test

Test task from Noveo to serve request and re-dispach them to multiple backends.


## Backends

Implemented backend types:
- GenericBackendInterface
- EmailBackendInterface (partial as dummy)
- LogBackendInterface
- TelegrambotBackendInterface
	
  
## Build	

Build using Dockerfile [`docker build -t noveo_test .`]
Preinstalled backends after container build:
- LogBackendInterface : path to log ./backend.log
- TelegrambotBackendInterface : subscribe Telegram channel [@TestServiceNoveoChannel](https://t.me/TestServiceNoveoChannel) to check notifications sending


## Run

Run docker image [`docker run -d -p 8000:8000 noveo_test`]
Open address http://127.0.0.1:8000/service/

Listener expects POST request with JSON data structure for notification: 
```
{
	"message": "notification text",
	"sender": "sender name",
	"sender_ip": "optional sender IP address"
}
```
Send JSON with notification using included Django DRF service http://127.0.0.1:8000/service/ or other external tool like POSTMAN.


## Management

There are few commands implemented to manage backends:
- [`python manage.py backend_type`]	- list of all implemented backend types (classes)
- [`python manage.py backend_list`]	- list of all registered backend
- [`python manage.py backend_notify`] - command for sending notification after application start up
- [`python manage.py backend_add -n "backend name" -t "backend type (classname)" -s "settings for the backend (JSON)"`]	- add new backend
- [`python manage.py backend_delete -i id`]	- delete backend with id
- [`python manage.py backend_manage -n "backend name" -s on|off`]	- switch on|off sending notification to backend
- [`python manage.py backend_settings -i id`]	- show settings for backend with id
	

## Tests

pytest


## How to improve design
1. Make token authentication
2. Use PostgreeSQL for the DBMS instead of SQLite
3. Use Celery for task management 


## Author
	Andrew Rabtsevich
