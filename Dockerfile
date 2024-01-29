# Stage 1: Train
FROM python:3.9-slim AS train
WORKDIR /app

Copy ./requirements.txt ./
COPY ml /app/ml
COPY ml/train-main.py /app/train-main.py

RUN pip install --no-cache-dir -r requirements.txt

# Run model training script
RUN python train-main.py

# Stage 2: Serving
FROM python:3.9-slim AS pack-serving
WORKDIR /app

# Copy model and preprocess pipeline from the train stage
COPY --from=train /app/final_model.pickle /app/api/model/final_model.pickle
COPY --from=train /app/preprocess_pipeline.pickle /app/api/model/preprocess_pipeline.pickle

COPY app/api/app.py app/api/app.py

RUN pip install flask

# Expose port to listen on
EXPOSE 5000

# Run the flask app
CMD ["python", "app.py"]
