# Makefile for EmpathAI Project

.PHONY: help install run format lint clean populate-kb docker-up docker-down docker-logs

# Default target: Tampilkan bantuan
help:
	@echo "Makefile for EmpathAI - Teman Curhat Psikologi"
	@echo ""
	@echo "Available commands:"
	@echo "  install      - Install/sync Python dependencies using uv"
	@echo "  run          - Run the Streamlit application locally"
	@echo "  format       - Format code using black and ruff"
	@echo "  lint         - Lint code using ruff"
	@echo "  populate-kb  - Populate the ChromaDB vectorstore with knowledge base documents"
	@echo "  docker-up    - Start the application using Docker Compose"
	@echo "  docker-down  - Stop the Docker Compose services"
	@echo "  docker-logs  - Follow logs from the Docker container"
	@echo "  clean        - Remove temporary Python files and caches"

# Dependency Management
install:
	@echo ">>> Installing dependencies with uv..."
	uv sync

# Running the Application
run:
	@echo ">>> Starting Streamlit application on http://localhost:8501"
	PYTHONPATH=. streamlit run src/main.py

# Code Quality
format:
	@echo ">>> Formatting code with black and ruff..."
	uv run black .
	uv run ruff check . --fix --show-fixes

lint:
	@echo ">>> Linting code with ruff..."
	uv run ruff check .

# Knowledge Base
populate-kb:
	@echo ">>> Populating Knowledge Base from 'data/knowledge'..."
	PYTHONPATH=. python -c "from src.psychology.knowledge_base import PsychologyKnowledgeBase; kb = PsychologyKnowledgeBase(); kb.add_documents()"

# Docker Commands
docker-up:
	@echo ">>> Starting application with Docker Compose in detached mode..."
	docker-compose up --build -d

docker-down:
	@echo ">>> Stopping Docker Compose services..."
	docker-compose down

docker-logs:
	@echo ">>> Following logs for the 'empathai' service..."
	docker-compose logs -f empathai

# Cleaning
clean:
	@echo ">>> Cleaning up temporary files and caches..."
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .pytest_cache .ruff_cache .coverage htmlcov/ build/ dist/ *.egg-info/