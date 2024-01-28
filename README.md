This is a simple project that does a few things in one repo.
It should be noted that the important part of this project is to show end-to-end MLOps pipeline. 
Therefore, the models are not optimized and the data is not super complicated.

The main focus is to get the whole pipeline working.

## ML module
This is the module that contains the ML code. 
The code is built in a way to be robust to different models, scoring functions etc. and I tried to make sure
it's production grade.

- Get data from locally OR (if not found locally, then) from a URL.
  - The data is about house prices.
  - It has 12 features and 1 target with the name "SalePrice".
- Preprocess the data and train 3 simple models.
  - Preprocessing includes:
    - Imputing missing values
    - Encoding categorical features using One Hot Encoding.
  - Models used:
    - Linear Regression
    - Support Vector Regressor
    - Random Forest Regressor
- Compare the models using a scoring function.
  - Default is RMSE but it can be configured to use other scoring functions.
- Choose the best model according to a predefined criteria and save the best model as
a pickle file.
  - The preprocessing pipeline should also be saved to be able to use in production the same way it was fit on the training data.

There are basic unittests for the ML module to make sure it's working as expected.
If in the future, there would be more models, more optimizations or different scoring functions
etc. then the unittests would make sure that the code is still working as expected.

## APP module
This is the module that contains the Flask app.
The chosen model is served using Flask and the app is dockerized.
The app a "/predict" endpoint that accepts a POST request.
The request should have a JSON body with the data to be predicted.

![Image](images/img.png)

## Containerization
The app is dockerized.
I used Docker multi-stage to first train all models and then use the best model to serve the app.

## CI/CD
The CI/CD is done using Github Actions.
There a few different workflows:
1) Unit tests - Runs the unittests for the ML module on each push to the repo.
2) Deploy to ECR - On each change to the main branch, the app is built and pushed to ECR with a new tag.
3) Deploy to Docker Hub - On each change to the main branch, the app is built and pushed to Docker Hub. 
This is actually not needed but I used to play around with the image etc. and testing.
4) Deploy EC2 machines - I used Terraform to deploy EC2 machines on AWS.

## Next Steps
I will separate it into 2 parts:
1) If I had more time
2) Longer term/more complete end-to-end solution

### If I had more time
- Add more unittests for the ML module.
- Separate to 2 repos:
  - It would be better to have one repo for serving and deploying the app and another repo for actual ML work.
  - This way, we could separate the ML research, different use cases and improvements for the models and/or parts of
  the pipeline from the actual serving and deployment. The serving and deployment should be agnostic to the model being used.
  - In the given structure, a small bug with the data used or other other ML/logic related bugs would be caught only when deployed
    (even though there are unittests for the ML module).

### More complete solution
The goal is to have a robust MLOps pipeline that distributes the work between different domain experts. Meaning, the 
data scientists can focus on the models and research on how to optimize the models and get more accurate predictions.
MLOps engineers can focus on serving and deployment without having to worry about the accuracy of the models or other possible
bugs in the ML code.

- Model Registry
  - In the current solution we don't really have a way to keep track of the models that were trained and deployed.
  - We could save each model to a registry and then the serving part would be able to pull the chosen model from the registry.
  - Writing to the registry could be done using a CI/CD pipeline including some necessary checks to make sure the models are as expected.
- Experiment Management
  - Instead of just defining one criteria and choosing the best model, we could keep track of different metrics in differnt 
  parts of the model training pipeline.
  - In a more complex model training pipeline, we probably would have HPS tuning, different models, different scoring functions etc.
- Periodic/Conditional Retraining
  - Instead of a push to this repo with new data and manually triggering the training and deployment, we could either have a
  periodic retraining (depending on the data) that can periodically check for new data from either the database or file storage and train.
  - Another option is to have a monitoring system on the model that could detect data drift and/or target drift and trigger a retraining.
- Separating the parts of the model training pipeline instead of having one big script.
  - This would allow us to improve different parts of the pipeline without having to change everything else.
  - This would also enable modularity and parallelization.
  - A workflow orchestrator could be used to manage the pipeline.
  - This way we could also track different versions of different parts.