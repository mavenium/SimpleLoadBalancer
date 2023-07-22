### How to execute?
- Install `docker` and `docker-compose` on your computer
- Clone the project `git clone --branch dev https://<token>@github.com/mavenium/SimpleLoadBalancer.git`

##### How to execute the backend servers?
- Go to the project directory `cd SimpleLoadBalancer/backend_servers`
- Create the network:
- `docker network create load_balancer_network`
- Build the image:
- `docker build -t server .`
- Run `docker-compose -f docker-compose.yml up -d` command
- Then run the browser and go to `http://127.0.0.1:8081/`
- The server ports are `8081, 8082, 8083, 8084`