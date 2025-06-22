.PHONY: deps run test

# baixa os requisitos do arquivo requiriments.txt
deps:
	pip install -r requirements.txt

# executa o main.py
run:
	python main.py

# roda os testes com verbosidade
test:
	pytest -v
