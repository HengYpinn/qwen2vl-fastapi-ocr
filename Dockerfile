# Use NVIDIA-supported PyTorch base for CUDA and GPU support
FROM pytorch/pytorch:2.1.0-cuda11.8-cudnn8-runtime

# Set work directory
WORKDIR /app

RUN apt-get update && apt-get install -y \
    git \
    poppler-utils \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

# Copy project files into the container
COPY . .

# Install Python dependencies
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Expose the FastAPI port
EXPOSE 8000

# Run the app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
