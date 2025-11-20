# Microservice Makefile
BANK_APP = Src.banking_service.banking:app
LOGIN_APP = Src.login_service.login:app
NOTIF_APP = Src.notification_service.notification:app
ORDER_APP = Src.order_service.orders:app
PID_FILE = .uvicorn.pid

install:
	pip install -r requirements.txt

freeze:
	pip freeze > requirements.txt

run:
	python -m uvicorn $(BANK_APP) --host 0.0.0.0 --port 8000 --reload

start:
	nohup python -m uvicorn $(BANK_APP) --host 0.0.0.0 --port 8000 --reload \
	> .uvicorn.out 2>&1 & echo $$! > $(PID_FILE)
	@echo "Banking service started (PID=$$(cat $(PID_FILE))) on http://localhost:8000"

stop:
	@if [ -f $(PID_FILE) ]; then \
	kill $$(cat $(PID_FILE)) && rm -f $(PID_FILE) && echo "Service stopped."; \
	else \
	echo "No PID file found. Did you use 'make start-[service]'?"; \
	fi

test:
	python -m pytest -q