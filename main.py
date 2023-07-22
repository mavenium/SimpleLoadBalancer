import http.server
import http.client

import threading

from LoadBalancer import LoadBalancerHandler


def start_load_balancer():
    """Simple function for starting the load balancer"""

    backend_servers = [
        {"host": "localhost", "port": 8081},
        {"host": "localhost", "port": 8082},
        {"host": "localhost", "port": 8083},
        {"host": "localhost", "port": 8084}
    ]
    load_balancer_host = "localhost"
    load_balancer_port = 8002

    handler = LoadBalancerHandler
    handler.backend_servers = backend_servers
    handler.current_server_id = 0

    server = http.server.HTTPServer((load_balancer_host, load_balancer_port), handler)

    print(f"Load Balancer started on {load_balancer_host}:{load_balancer_port}")

    server.serve_forever()


if __name__ == "__main__":
    # Start the load balancer in a separate thread
    load_balancer_thread = threading.Thread(target=start_load_balancer)
    load_balancer_thread.start()
