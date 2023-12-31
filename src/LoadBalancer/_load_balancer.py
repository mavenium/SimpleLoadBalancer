from http import server, client

import logging

logging.basicConfig(
    filename='logging.log',
    level=logging.DEBUG,
    format='%(asctime)s:%(levelname)s:%(name)s:%(message)s',
    filemode='w'
)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


class LoadBalancerHandler(server.SimpleHTTPRequestHandler):
    backend_servers = []
    current_server_id = 0
    connection_timeout = 1

    def __setattr__(self, key, value) -> None:
        """It will use for changing the value of class attrs"""
        backend_servers = value if key == 'backend_servers' else []
        current_server_id = value if key == 'current_server_id' else 0
        connection_timeout = value if key == 'connection_timeout' else 1
        super(LoadBalancerHandler, self).__setattr__(key, value)

    @classmethod
    def get_backend_server(cls):
        """It returns the server backend by 'current_server_id' value"""
        return cls.backend_servers[cls.current_server_id]

    @classmethod
    def move_to_next_backend_server(cls):
        """This value specifies the 'current_server_id'"""
        # (Round-Robin) algorithm
        cls.current_server_id = (cls.current_server_id + 1) % len(cls.backend_servers)
        logger.info(f"Current server id is : {cls.current_server_id}")

    def do_GET(self):
        try:
            # Retrieve the backend server details
            current_server = self.get_backend_server()

            # Send a request to the backend server
            connection = client.HTTPConnection(
                host=current_server["host"],
                port=current_server["port"],
                timeout=float(self.connection_timeout)
            )
            connection.request("GET", self.path)
            response = connection.getresponse()

            print(f"Response From {current_server['host']}:{current_server['port']} Status {response.status}")
            logger.info(f"Response From {current_server['host']}:{current_server['port']} Status {response.status}")

            # Return the response from the backend server to the client
            self.send_response(response.status)
            self.send_header("Content-type", response.headers.get("Content-type"))
            self.end_headers()
            self.wfile.write(response.read())

            # Close the connection to the backend server
            connection.close()
        except Exception as e:
            # Handle any exceptions and move to the next server
            self.move_to_next_backend_server()
            logger.error(f"Error 500! {str(e)}")
            self.send_error(500, str(e))
