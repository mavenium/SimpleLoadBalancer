import http.server
import http.client

import threading

import logging

from os import environ

from LoadBalancer import LoadBalancerHandler

logging.basicConfig(
    filename='logging.log',
    level=logging.DEBUG,
    format='%(asctime)s:%(levelname)s:%(name)s:%(message)s',
    filemode='w'
)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def start_load_balancer():
    """Simple function for starting the load balancer"""

    backend_servers = [
        {"host": environ["BACKEND_SERVER_ONE"], "port": environ["BACKEND_SERVER_ONE_PORT"]},
        {"host": environ["BACKEND_SERVER_TWO"], "port": environ["BACKEND_SERVER_TWO_PORT"]},
        {"host": environ["BACKEND_SERVER_TREE"], "port": environ["BACKEND_SERVER_TREE_PORT"]},
        {"host": environ["BACKEND_SERVER_FOUR"], "port": environ["BACKEND_SERVER_FOUR_PORT"]}
    ]
    load_balancer_host = "0.0.0.0"
    load_balancer_port = 8080

    handler = LoadBalancerHandler
    handler.backend_servers = backend_servers
    handler.current_server_id = 0
    handler.connection_timeout = environ["CONNECTION_TIMEOUT"]

    server = http.server.HTTPServer((load_balancer_host, load_balancer_port), handler)

    print(f"Load Balancer started on {load_balancer_host}:{load_balancer_port}")
    logger.info(f"Load Balancer started on {load_balancer_host}:{load_balancer_port}")

    server.serve_forever()


if __name__ == "__main__":
    # Start the load balancer in a separate thread
    load_balancer_thread = threading.Thread(target=start_load_balancer)
    load_balancer_thread.start()
