# Multi-stage build for optimized image
FROM python:3.11-slim as builder

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
# Install dependencies into the system site-packages (not --user)
RUN pip install --no-cache-dir -r requirements.txt

# Final stage
FROM python:3.11-slim

WORKDIR /app

# Copy Python dependencies from builder system site-packages/binaries
COPY --from=builder /usr/local /usr/local

# Copy application code
COPY . .

# Ensure pip-installed console scripts are on PATH
ENV PATH=/usr/local/bin:$PATH

EXPOSE 5000

# Use gunicorn in production
ENV FLASK_ENV=production
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:5000", "oriyan_portfolio:app"]
