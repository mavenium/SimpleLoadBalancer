from http import server, client


class LoadBalancerHandler(server.SimpleHTTPRequestHandler):
    backend_servers = []
    current_server_id = 0

    def __setattr__(self, key, value) -> None:
        """It will use for changing the value of class attrs"""
        backend_servers = value if key == 'backend_servers' else []
        current_server_id = value if key == 'current_server_id' else 0
        super(LoadBalancerHandler, self).__setattr__(key, value)

    @classmethod
    def get_backend_server(cls):
        """It returns the server backend by 'current_server_id' value"""
        return cls.backend_servers[cls.current_server_id]

    @classmethod
    def move_to_next_backend_server(cls):
        """It sets the 'current_server_id' value based on (Round-Robin) algorithm"""
        cls.current_server_id = (cls.current_server_id + 1) % len(cls.backend_servers)

    def do_GET(self):
        try:
            # Retrieve the backend server details
            current_server = self.get_backend_server()

            # Send a request to the backend server
            connection = client.HTTPConnection(current_server["host"], current_server["port"])
            connection.request("GET", self.path)
            response = connection.getresponse()

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
            self.send_error(500, str(e))
