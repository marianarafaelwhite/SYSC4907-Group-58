# Kubernetes Configuration files

## Quick startup guide

1. Install minikubes on a machine

    https://minikube.sigs.k8s.io/docs/start/

1. Install Docker
   
    https://docs.docker.com/get-docker/

1. Switch to minikube env and build docker images
    ```
    $(minikube docker-env)
    docker build -t sysc4907_group58/base -f dockerfiles/base/Dockerfile .
    docker build -t sysc4907_group58/classifier -f dockerfiles/classifier/Dockerfile .
    docker build -t sysc4907_group58/server -f dockerfiles/server/Dockerfile .
    ```
1. Create deployments using the configuration files, which in term use the images produced in previous step
    ```
    kubectl create -f classifier.yml 
    kubectl create -f app_co2.yml 
    kubectl create -f app_humidity.yml 
    ```
1. Create service from the deployments, note that --name= produces an internally resoluble hostname
    ```
    kubectl expose deployment classifier --type=NodePort --protocol=UDP
    kubectl expose deployment app-humidity --type=NodePort --name=app-humidity --protocol=UDP
    kubectl expose deployment app-co2 --type=NodePort --name=app-co2 --protocol=UDP
    ```
1. figure what ip/port to be used in to accept traffic
    ```
    $minikube service list

    |----------------------|---------------------------|--------------|---------------------------|
    |      NAMESPACE       |           NAME            | TARGET PORT  |            URL            |
    |----------------------|---------------------------|--------------|---------------------------|
    | default              | app-co2                   |         7777 | http://192.168.49.2:30735 |
    | default              | app-humidity              |         7777 | http://192.168.49.2:32005 |
    | default              | classifier                |         7777 | http://192.168.49.2:32388 |
    | default              | kubernetes                | No node port |
    | kube-system          | kube-dns                  | No node port |
    | kubernetes-dashboard | dashboard-metrics-scraper | No node port |
    | kubernetes-dashboard | kubernetes-dashboard      | No node port |
    |----------------------|---------------------------|--------------|---------------------------|

    ```

    In this case it will be 192.168.49.2:32388. Note that this needs to be run on the same machine, 
    still need to figure out how to make it accessible from a different machine.
   
1. Send some traffic to the classifier
   ```
   python3 hardware_emulator.py -v -ip 192.168.49.2 -p 32388
   ```
   
1. Launch the dashboard in a separate terminal
   ``` 
    minikube dashboard
   ```
   You can then click the three dot on the right side of a running pod, and click execute to bring up shell
   
    Try checking the logfile located at /tmp/logfile

## Redeploy with an updated version of docker image which contains script
for example
1. rebuild image
   ```
   docker build -t sysc4907_group58/classifier -f dockerfiles/classifier/Dockerfile .
   ```
2. roll out the change to the deployment
   ```
   kubectl rollout restart deployment/classifier
   ``` 
