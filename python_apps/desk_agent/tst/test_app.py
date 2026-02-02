from ..src import app
import requests
import requests_mock

def test_handler(requests_mock):
    
    # Mock the API Gateway Endpoint
    url = "https://fakeendpoint.com"
    app.api_endpoint = url
    requests_mock.post(url, text='ok')
   
   
    app.handler({}, None)