import pytest

from . import index

def test_handler_returns_status_code_200():
    event = {}
    context = {}
    
    response = index.handler(event, context)
    
    assert response['statusCode'] == 200