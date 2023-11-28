# Project

The goal of `project` is to take everything you've learned about managing deployments, performance, and testing for your application which has been deployed on `Azure Kubernetes Service (AKS)`.

- Package up an NLP model ([DistilBERT](https://arxiv.org/abs/1910.01108)) for running efficient CPU-based inferencing for POSITIVE/NEGATIVE sentiment 
- Have results be cached to protect your endpoint from abuse
- Use `grafana` to understand the dynamics of your system.
- Leverage `k6` to load test your `/predict` endpoint
- Leverage `pytest` to ensure that your application works correctly prior to deployment on `AKS`.
- Leverage `poetry` to manage your runtime environment in a portable way.
- Leverage `Docker` to package applications in a reuseable fashion

While this project is serving an NLP model. We do not want you focused on specific implementation details of the model. Model training, loading, and prediction pipeline is handled for you already in the provided implementation.

Please review the `train.py` to see how the model was trained and pushed to `HuggingFace` as an artifact store for models and their associated configuration. This model took 5 minutes to transfer learn on 2x A4000 GPUs with a 256 batch size, taking 15 GB of memory on each GPU. Training on CPUs would likely have taken several days. The given implementation allows for a maximum text sequences of 512 tokens for each input.

Model loading examples are provided in `mlapi/example.py` in this file we directly load the model from `HuggingFace` however this is extremely inefficient given the size of the underlying model (256 MB) for a production enviornment. We will pull down the model locally as part of our build process. 

Model prediction pipelines are included in the `transformers` API provided by `HuggingFace` which dramatically reduces the amount of complexity in the Inferencing application. Example is provided in `mlapi/example.py` and is instrumented already in your `mlapi/main.py` application.

## Helpful Information

Do not run `poetry update` it will take a long time due to the handling of `torch` dependencies.

You might need to install `git lfs` <https://git-lfs.github.com/>
```{bash}
brew install git-lfs
apt install git-lfs
```

## Requirements

1. Write pydantic models to meet the specified input model:
```
{"text": ["example 1", "example 2"]}
```
2. Pull the following model [winegarj/distilbert-base-uncased-finetuned-sst2](https://huggingface.co/winegarj/distilbert-base-uncased-finetuned-sst2) locally to allow for loading into your application. Put this at the root of your project directory for an easier time.
3. Run pytest to ensure your application is working as intended.
    - Update your application as neccessary
4. Build and test your docker container locally. 
    - Minikube or docker-compose are fine. 
    - `kustomize` overlays and `docker-compose.yml` files are provided to minimize effort
5. Push your image to ACR use a prefix based on your namespace, and call the image project.
6. Deploy your application to AKS leveraging Istio similarly to `lab 4/5`
7. Test your endpoint works with a simple example
8. If your endpoint is unresponsive, make sure you review the pods and logs and see if there are any issues.
9. Run k6 against your endpoint with the provided `load.js`
10. Feel extremely proud about all the learning you went through over the semester and how this will help you develop professionally and enable you to deploy an API effectively during capstone. There is much to learn, but getting the fundamentals are key.

## Submission

All code will be graded off your repo's `main` branch. No additional forms or submission processes are needed.

## Grading

Grades will be given based on the following:

1. Adhesion to requirements and rubric

### Rubric

All items are conditional on a `95%` cache rate, and after a `10 minute` sustained load:

- `pytest` (provided) pass for your project: 2 point
- `Model` is loaded into the container as part of the build process instead of being dynamically pulled down from `HuggingFace` on model instantiation: 2 point
- Ability to hit `/predict` endpoint and get sentiment responses: 2 points
- Ability to hit `/predict` endpoint 10/s: 2 points
- p(99) < 2 second for `/predict` endpoint under 10 Virtual User (`k6` VU) load: 2 points


## Time Expectations

This project will take approximately ~10 hours. 