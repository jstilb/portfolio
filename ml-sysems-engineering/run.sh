#!/bin/bash
NAMESPACE=jmstilb
APP_NAME=project
IMAGE_NAME="${NAMESPACE}/${APP_NAME}"
ACR_DOMAIN=w255mids.azurecr.io
IMAGE_FQDN="${ACR_DOMAIN}/${IMAGE_NAME}"


# remove kube prior to running
kubectl delete -k mlapi/.k8s/overlays/dev
kubectl delete -k mlapi/.k8s/overlays/prod


# stop and remove image in case this script was run before
docker rmi -f ${IMAGE_NAME}
docker rmi -f ${IMAGE_FQDN}


# start minikube
kubectl config use-context w255-aks
az acr login --name w255mids


# rebuild and run the new image
cd mlapi
docker build -t ${IMAGE_NAME} .

# create tag
TAG=$(openssl rand -hex 4)
sed "s/\[TAG\]/${TAG}/g" .k8s/overlays/prod/patch-deployment-project.yaml


# tag container, push, and pull
docker tag ${IMAGE_NAME} ${IMAGE_FQDN}:${TAG}
docker push ${IMAGE_FQDN}:${TAG}
docker pull ${IMAGE_FQDN}:${TAG}


# kubernetes deployment
kubectl kustomize .k8s/overlays/prod
kubectl apply -k .k8s/overlays/prod


# wait for the /health endpoint to return a 200 and then move on
finished=false
while ! $finished; do
    health_status=$(curl -o /dev/null -s -w "%{http_code}\n" -X GET "http://${NAMESPACE}.${DOMAIN}/health" -L)
    if [ $health_status == "200" ]; then
        finished=true
        echo "API is ready"
    else
        echo "API not responding yet"
        sleep 5
    fi
done

curl -X 'POST'  'https://jmstilb.mids-w255.com/predict' -H 'accept: application/json' -H 'Content-Type: application/json' -d '{"text": ["I like it but I dont love it"]}'