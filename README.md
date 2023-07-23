### How to execute?
- Install `docker` and `docker-compose` on your computer
- Clone the project `git clone --branch dev https://<token>@github.com/mavenium/SimpleLoadBalancer.git`

##### Create the network
- Create the network:
- `docker network create load_balancer_network`

##### How to build the backend servers image?
- Go to the `backend_servers` directory `cd SimpleLoadBalancer/backend_servers`
- Build the image:
- `docker build -t server .`

##### How to build the load balancer image?
- Go to the project directory `cd SimpleLoadBalancer`
- Build the image:
- `docker build -t load_balancer .`

##### How to run?
- Go to the project directory `cd SimpleLoadBalancer`
- Run `docker-compose -f docker-compose.yml --compatibility up -d` command
- Then run the browser and go to `http://127.0.0.1:8080/` for access the load balancer service
- The server ports are `8081, 8082, 8083, 8084` so you can access to them directly by `http://127.0.0.1:8081/`

### How to monitor?
- You can use this command to view the stats of containers
```
 docker stats load_balancer server_one server_two server_tree server_four
```

### How to see the logs?
- By executing the `load_balancer` container `docker exec -it load_balancer bash`
- Then you can see the logs by this command `tail -f logging.log`

### How to send the lot of request?
- You need the `node` image `docker pull node:latest`
- Create a container and bind to the `load_balancer_network` network
```
docker run -itd --name load_tester --cpus 2 --memory 2g --network load_balancer_network node:latest
```
- Next, install the `loadtest` package on this container `npm install -g loadtest`
- After that, update and install some packages `apt-get update && apt-get install -y curl nano`
- Now you can send a lot of request to the load balancer system `loadtest -c 1 --rps 1 http://load_balancer:8080`