# Kubernetes Configuration files
TODO:
- [ ] review/update all the label/names, e.g. classifier probably shouldn't be app?
- [ ] consider using different port number for each pod to differentiate them?
- [ ] review/optimize whatever relevant configurations in the yml

## Quick startup guide
1. Install Docker
   
    https://docs.docker.com/get-docker/

1. Install and start minikube on a machine

    https://minikube.sigs.k8s.io/docs/start/

1. Switch to minikube env and build docker images.
   If the docker images are built outside the env, Kubernetes won't be able to find them.
    ```bash
    $(minikube docker-env)
    docker build -t sysc4907_group58/base -f dockerfiles/base/Dockerfile .
    docker build -t sysc4907_group58/classifier -f dockerfiles/classifier/Dockerfile .
    docker build -t sysc4907_group58/server -f dockerfiles/server/Dockerfile .
    ```
1. Create Kubernetes resources with the provided configuration files located inside k8s/ folder
    ```bash
    kubectl create -f k8s
    ```

    Basically each configuration will create deployment describing what the pods should be running, and services defines
    the sets of pods running the application and how to access them.

    Take a look at the following documentation as well.

    https://kubernetes.io/docs/tutorials/kubernetes-basics/
    https://kubernetes.io/docs/concepts/services-networking/service/
    https://kubernetes.io/docs/concepts/workloads/controllers/deployment/

1. figure out the ip:port combination to receive the IoT traffic.
    ```bash
    echo $(minikube ip):$(kubectl get services/classifier -o go-template='{{(index .spec.ports 0).nodePort}}')

    ```

    It will mostly likely be 192.168.49.2:32388 because minikube seems to run on that ip by default, and the
    **nodePort** of the classifier has been set to 32888 in _classifier.yml_
   
1. Send some traffic to the classifier service running on our node.
   ```bash
   python3 hardware_emulator.py -v -ip 192.168.49.2 -p 32388
   ```
   
   Let's check whether the app behind the classifier is receiving the traffic.

   First figure out the name of a pod running the data processing application.
   ```bash
   export POD_NAME=$(kubectl get pods -l app=app-co2 -o go-template --template '{{range .items}}{{.metadata.name}}{{"\n"}}{{end}}')
   echo Name of the Pod: $POD_NAME
   ```

   Then tail the logfile of our application

   ```bash
   kubectl exec $POD_NAME -- tail -f /tmp/logfile.log
   ```

1. [Optional] Launch and play with the  dashboard in a separate terminal
   ```bash
    minikube dashboard
   ```
   You can then click the three dot on the right side of a running pod, and click execute to bring up shell

## Rapid redeploy an updated version of image to a deployment during R&D
Using classifier as an example

1. rebuild image, the build process copies the iot script folder into the image.
   ```bash
   docker build -t sysc4907_group58/classifier -f dockerfiles/classifier/Dockerfile .
   ```
1. roll out the change to the deployment
   ```bash
   kubectl rollout restart deployment/classifier
   ``` 
