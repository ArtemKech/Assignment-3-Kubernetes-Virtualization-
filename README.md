# Assignment-3-Kubernetes-Virtualization-
This `README` contains steps for the assignment including screenshots of command executions

# Creation of clusters
### Staging and Production Clusters creation

```shell
gcloud container clusters create-auto production --location=us-central1
gcloud container clusters create-auto staging --location=us-central1
```
![image](https://github.com/ArtemKech/Assignment-3-Kubernetes-Virtualization-/assets/84817894/d1e05be6-bef6-4a57-b7e7-0f004d9380ba)

---

### Authenticate kubectl

```shell
gcloud container clusters get-credentials production --zone=us-central1
gcloud container clusters get-credentials staging --zone=us-central1
```

# Redis deployment

### Create `redis-deployment.yaml`

```shell
apiVersion: apps/v1
kind: Deployment
metadata:
  name: redis-deployment
spec:
    replicas: 1
    selector:
       matchLabels:
         app: redis
    template:
       metadata:
         labels:
          app: redis
       spec:
         containers:
         - name: redis
           image: redis:latest
           ports:
           - containerPort: 6379
```
![image](https://github.com/ArtemKech/Assignment-3-Kubernetes-Virtualization-/assets/84817894/43ce3eef-7d93-4c36-b141-e5a71a02c0bb)

---

### Apply created configuration

```shell
kubectl apply -f redis-deployment.yaml
```

---

### Create a Cluster IP Service

```shell
apiVersion: v1
kind: Service
metadata:
  name: redis-service
spec:
  selector:
    app: redis
  ports:
    - protocol: TCP
      port: 6379  # Redis default port
      targetPort: 6379
  type: ClusterIP
```
![image](https://github.com/ArtemKech/Assignment-3-Kubernetes-Virtualization-/assets/84817894/007a15ec-d34e-4ca1-b706-0acae7fc0335)

---

### Apply created configuration

```shell
kubectl apply -f redis-service.yaml
```
![image](https://github.com/ArtemKech/Assignment-3-Kubernetes-Virtualization-/assets/84817894/e6191651-5520-45c2-a12f-88d4b891f858)

---

### ConfigMap for Redis Configuration

```shell
apiVersion: v1
kind: ConfigMap
metadata:
  name: redis-config
data:
  REDIS_HOST: redis-service
  REDIS_PORT: "6379"
```
![image](https://github.com/ArtemKech/Assignment-3-Kubernetes-Virtualization-/assets/84817894/061b5c24-b088-4c3d-b3d8-3ccb00fe5396)

---

### Apply created configuration

```shell
kubectl apply -f redis-configmap.yaml

```
![image](https://github.com/ArtemKech/Assignment-3-Kubernetes-Virtualization-/assets/84817894/8f07cbaa-8053-41fa-91fe-81e65ccaa204)


---

### Verify the Redis Deployment

```shell
kubectl get deployment redis-deployment
kubectl get pods -l app=redis
```

![image](https://github.com/ArtemKech/Assignment-3-Kubernetes-Virtualization-/assets/84817894/4e0cff47-fad0-4784-955d-d5328d6c2fff)

# Deployment of Flask application on Kubernetes

### Create a repository with 2 branches `staging` & `production`

Upload the code from Teams to GitHub repo

---

### Build a Docker Image

```docker
docker build -t flask-app-image .
```

---

### Tag the Docker image with the registry path

```docker
docker tag flask-app-image:latest gcr.io/vast-service-390209/flask-app:latest
```

---

### Push the tagged image to the container registry

```docker
docker push gcr.io/vast-service-390209/flask-app:latest
```

---

### Create Kubernetes Deployment file `flask-app-deployment.yaml`

```shell
apiVersion: apps/v1
kind: Deployment
metadata:
  name: flask-app-deployment
spec:
  replicas: 2
  selector:
    matchLabels:
      app: flask-app
  template:
    metadata:
      labels:
        app: flask-app
    spec:
      containers:
        - name: flask-app-container
          image: gcr.io/vast-service-390209/flask-app/flask-app:latest
          ports:
            - containerPort: 5000
```

---

### Apply deployment config

```shell
kubectl apply -f flask-app-deployment.yaml
```
![image](https://github.com/ArtemKech/Assignment-3-Kubernetes-Virtualization-/assets/84817894/3e7495db-87bb-4c6a-8406-556893f3be20)

---

### Expose the Flask App with Load Balancer

Create `flask-app-load-balancer-service.yaml` file with:

```shell
apiVersion: v1
kind: Service
metadata:
  name: flask-app-service
spec:
  selector:
    app: flask-app
  ports:
    - protocol: TCP
      port: 80
      targetPort: 5000
  type: LoadBalancer
```

---

### Apply service

```shell
kubectl apply -f flask-app-service.yaml
```
![image](https://github.com/ArtemKech/Assignment-3-Kubernetes-Virtualization-/assets/84817894/3778f05e-5385-4ba5-bb69-809b2c3f0046)

# Set up a CI/CD pipeline

### Enabled Google Cloud Build API

---

### Create `cloudbuild.yaml` file

It should be located inside the repository of the Flask App
Add the following:

```shell
steps:
- name: 'gcr.io/cloud-builders/docker'
  args:
  - 'build'
  - '-t'
  - 'gcr.io/vast-service-390209/flask-app-image:$COMMIT_SHA=$(git rev-parse --short HEAD)'
  - '.'
- name: 'gcr.io/cloud-builders/kubectl'
  args:
  - 'apply'
  - '-f'
  - 'k8s/deployment.yaml'
  env:
  - 'CLOUDSDK_COMPUTE_ZONE=us-central1'
  - 'CLOUDSDK_CONTAINER_CLUSTER=gke_vast-service-390209_us-central1_staging'
images:
  - 'gcr.io/vast-service-390209/flask-app-image:$COMMIT_SHA=$(git rev-parse --short HEAD)'
substitutions:
  _CLUSTER_NAME: staging
  

logsBucket: 'gs://logs-fadsladasasdsk-asadspp-budasdsckedst'
```

---

### CI/CD Pipeline Configuration
Create the trigger & Link GitHub repository to your trigger
Once the changes to your branch done, it should show up on the list in triggers section:
![image](https://github.com/ArtemKech/Assignment-3-Kubernetes-Virtualization-/assets/84817894/7703cf21-fbe3-44d2-bc53-980280fa46fd)


![image](https://github.com/ArtemKech/Assignment-3-Kubernetes-Virtualization-/assets/84817894/86bd51b3-790c-4397-b4f5-32167e055c88)

# Checking deployment

### Check external IP of Flask App

```shell
kubectl get services
```

![image](https://github.com/ArtemKech/Assignment-3-Kubernetes-Virtualization-/assets/84817894/be999b3f-00b4-44a3-8e68-78f504b10043)

---

### Access it with:

```shell
http://external_ip
```


