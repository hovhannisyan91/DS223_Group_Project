FROM python:3.13-slim

WORKDIR /app

# Copy pyproject.toml
COPY pyproject.toml .

# Install dependencies
RUN pip install --no-cache-dir -e .

# Copy app code
COPY . .

# Expose port
EXPOSE 8501

# Run the app
CMD ["streamlit", "run", "main.py", "--server.port", "8501", "--server.address", "0.0.0.0"]