import requests
import json
import webbrowser
from api_keys import client_id, client_secret, redirect_uri
from urllib.parse import urlencode, urlparse, parse_qs
from loguru import logger
import requests
import base64
from urllib.parse import urlparse, parse_qs
import socket

def get_auth_code():
    auth_url = "https://accounts.spotify.com/authorize"
    auth_params = {
        "client_id": client_id,
        "response_type": "code",
        "redirect_uri": redirect_uri,
        "scope": "user-library-read playlist-read-private playlist-modify-public playlist-modify-private user-library-modify",
    }
    # Open authorization URL in the default web browser
    webbrowser.open(f"{auth_url}?{urlencode(auth_params)}")
    
    # Create a socket to listen for the redirect
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind(('localhost', 5000))  # Listening on port 5000
        server_socket.listen(1)
        logger.info("Waiting for authorization code...")
        
        # Accept a single connection and read the response
        client_socket, addr = server_socket.accept()
        with client_socket:
            request = client_socket.recv(1024).decode()
            # Parse the code from the URL
            request_line = request.split("\r\n")[0]
            redirect_url = "http://" + request_line.split(" ")[1]
            parsed_url = urlparse(redirect_url)
            auth_code = parse_qs(parsed_url.query)['code'][0]
            
            # Send a simple response back to the browser
            client_socket.sendall(b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nAuthorization code received. You can close this window.")
            logger.success("Authorization code received.")
    return auth_code


def get_access_token(client_id, client_secret, redirect_uri):
    # Step 2: Get the authorization code from the redirect URL
    auth_code = get_auth_code()
    
    # Step 3: Exchange the authorization code for an access token
    token_url = "https://accounts.spotify.com/api/token"
    token_data = {
        "grant_type": "authorization_code",
        "code": auth_code,
        "redirect_uri": redirect_uri,
    }
    # Encode client_id and client_secret in base64 and add to headers
    token_headers = {
        "Authorization": "Basic " + base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
    }
    
    # Request access token
    token_response = requests.post(token_url, data=token_data, headers=token_headers)
    token_response_data = token_response.json()
    
    # Check for a successful response
    if token_response.status_code == 200:
        access_token = token_response_data.get("access_token")
        print("Access token:", access_token)
        return access_token
    else:
        print("Failed to get access token:", token_response_data)
        return None
