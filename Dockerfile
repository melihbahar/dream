# Stage 1: Train the model
FROM python:3.9-slim AS train
WORKDIR /app

Copy ./requirements.txt ./

# Copy ml directory
COPY ml /app/ml

# Copy train script and requirements
COPY ml/train-main.py /app/train-main.py

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the training script
RUN python train-main.py

# Stage 2: Package serving
FROM python:3.9-slim AS pack-serving

# Copy trained model from the train stage
WORKDIR /app

COPY --from=train /app/final_model.pickle /app/api/model/final_model.pickle
COPY --from=train /app/preprocess_pipeline.pickle /app/api/model/preprocess_pipeline.pickle

# Copy Flask app
COPY app/api/app.py app/api/app.py

# Install Flask and other dependencies
RUN pip install flask

# Expose port
EXPOSE 5000

# Command to run the Flask app
CMD ["python", "app.py"]