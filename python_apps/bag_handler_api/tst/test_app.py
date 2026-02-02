from ..src import app

def test_handler():
    result = app.request_bag_handler({}, None)
    assert result['statusCode'] in [200,429]
    