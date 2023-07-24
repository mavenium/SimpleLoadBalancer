from http.server import HTTPServer

from threading import Thread

from time import sleep

from unittest.mock import patch, Mock
import unittest

from LoadBalancer import LoadBalancerHandler

from io import BytesIO as IO

import requests


class LoadBalancerTest(unittest.TestCase):

    def setUp(self) -> None:
        self.__backend_servers = [
            {"host": "localhost", "port": 8081},
            {"host": "localhost", "port": 8082},
            {"host": "localhost", "port": 8083},
            {"host": "localhost", "port": 8084}
        ]

    def test_get_backend_server(self):
        """Test getting the current backend server"""
        handler = LoadBalancerHandler
        handler.backend_servers = self.__backend_servers
        handler.current_server_id = 0
        server = handler.get_backend_server()

        # Asserts
        self.assertEqual(server, {"host": "localhost", "port": 8081})

    def test_move_to_next_backend_server(self):
        """Test moving to the next backend server"""
        handler = LoadBalancerHandler
        handler.backend_servers = self.__backend_servers
        handler.current_server_id = 0
        handler.move_to_next_backend_server()
        server = handler.get_backend_server()

        # Asserts
        self.assertEqual(server, {"host": "localhost", "port": 8082})
        self.assertEqual(handler.current_server_id, 1)

    @patch('http.server.HTTPServer')
    @patch('LoadBalancer.LoadBalancerHandler.do_GET')
    def test_do_get(self, mock_do_get, mock_http_server):
        """Test if you do_GET method gets called"""
        mock_request = Mock()
        mock_do_get.return_value = "/"
        mock_request.makefile.return_value = IO(b"GET /")
        server = LoadBalancerHandler(mock_request, ('localhost', 8080), mock_http_server)

        # Asserts
        self.assertTrue(mock_do_get.called)
        self.assertEqual(server.do_GET(), "/")


class IntegrationTests(unittest.TestCase):
    def setUp(self):
        handler = LoadBalancerHandler
        handler.backend_servers = [
            {"host": "localhost", "port": 8081},
            {"host": "localhost", "port": 8082},
            {"host": "localhost", "port": 8083},
            {"host": "localhost", "port": 8084}
        ]

        # Start the load balancer server
        self.host = "localhost"
        self.port = 8090
        self.server = HTTPServer((self.host, self.port), handler)
        self.server_thread = Thread(target=self.server.serve_forever)
        self.server_thread.start()

        # Wait for the server to start
        sleep(1)

    def tearDown(self):
        # Stop the load balancer server
        self.server.shutdown()
        self.server_thread.join()

    def test_load_balancer(self):
        # Send a GET request to the load balancer
        response = requests.get(f"http://{self.host}:{self.port}")

        # Assert that the response is successful (200)
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
