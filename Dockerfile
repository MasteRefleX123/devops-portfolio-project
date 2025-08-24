# Multi-stage build for optimized image
FROM python:3.11-slim as builder

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Final stage
FROM python:3.11-slim

WORKDIR /app

# Copy Python dependencies from builder
COPY --from=builder /root/.local /root/.local

# Copy application code
COPY . .

# Make sure scripts in .local are usable
ENV PATH=/root/.local/bin:$PATH

EXPOSE 5000

# Use gunicorn in production
ENV FLASK_ENV=production
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:5000", "oriyan_portfolio:app"]
