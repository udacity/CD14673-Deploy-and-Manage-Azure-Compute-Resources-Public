import json
import os
import uuid
import decimal
from boto3.dynamodb.types import DYNAMODB_CONTEXT
import boto3

TABLE_NAME = os.environ.get("TABLE_NAME", "CartTable")

dynamodb = boto3.resource("dynamodb")
_table = dynamodb.Table(TABLE_NAME)

PRODUCTS = [
    {"id": "p-001", "name": "Reusable Water Bottle", "price": 18.99},
    {"id": "p-002", "name": "Wireless Mouse", "price": 29.99},
    {"id": "p-003", "name": "Notebook Set", "price": 12.50},
    {"id": "p-004", "name": "Travel Mug", "price": 16.00},
]


# Convert float values to Decimal with DynamoDB-friendly context.
# This ensures that prices are stored with appropriate precision and scale.
def _round_float_to_decimal(float_value):
    with decimal.localcontext(DYNAMODB_CONTEXT) as ctx:
        # Allow rounding and inexact traps to be suppressed
        ctx.traps[decimal.Inexact] = 0
        ctx.traps[decimal.Rounded] = 0
        decimal_value = ctx.create_decimal_from_float(float_value)
    return decimal_value


# Serialize Decimal values to JSON-friendly floats.
# This is necessary for API responses using json.dumps since DynamoDB uses Decimal for numeric types.
def _decimal_serializer(obj):
    if isinstance(obj, decimal.Decimal):
        return float(obj)
    raise TypeError("Object of type %s is not JSON serializable" % type(obj).__name__)


# Build a standard API response payload.
def _response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
        },
        "body": json.dumps(body, default=_decimal_serializer),
    }


# Parse JSON request body into a dictionary.
def _parse_body(event):
    if not event.get("body"):
        return {}
    try:
        return json.loads(event["body"])
    except json.JSONDecodeError:
        return {}


# Scan the entire cart table and return all items.
def _scan_cart():
    items = []
    response = _table.scan()
    items.extend(response.get("Items", []))
    while "LastEvaluatedKey" in response:
        response = _table.scan(ExclusiveStartKey=response["LastEvaluatedKey"])
        items.extend(response.get("Items", []))
    return items


# Return the static product list.
def _handle_products():
    return _response(200, {"items": PRODUCTS})


# Return all items currently in the cart.
def _handle_get_cart():
    items = _scan_cart()
    return _response(200, {"items": items})


# Add a new item to the cart.
def _handle_add_to_cart(event):
    body = _parse_body(event)
    item_id = body.get("itemId") or body.get("id") or f"item-{uuid.uuid4()}"
    name = body.get("name") or "Untitled"
    price = _round_float_to_decimal(float(body.get("price") or 0))
    quantity = int(body.get("quantity") or 1)

    item = {
        "itemId": item_id,
        "name": name,
        "price": price,
        "quantity": quantity,
    }

    _table.put_item(Item=item)
    return _response(201, item)


# Update the quantity for an item in the cart.
def _handle_update_item(item_id, event):
    body = _parse_body(event)
    quantity = int(body.get("quantity") or 1)

    response = _table.update_item(
        Key={"itemId": item_id},
        UpdateExpression="SET quantity = :q",
        ExpressionAttributeValues={":q": quantity},
        ReturnValues="ALL_NEW",
    )
    return _response(200, response.get("Attributes", {}))


# Delete an item from the cart by ID.
def _handle_delete_item(item_id):
    _table.delete_item(Key={"itemId": item_id})
    return _response(200, {"deleted": item_id})


# Route Lambda events to the correct handler.
def lambda_handler(event, _context):
    method = event.get("httpMethod", "")
    path = event.get("path", "")
    path_parameters = event.get("pathParameters") or {}

    if method == "GET" and path.endswith("/products"):
        return _handle_products()

    if method == "GET" and path.endswith("/cart"):
        return _handle_get_cart()

    if method == "POST" and path.endswith("/cart"):
        return _handle_add_to_cart(event)

    if method == "PUT" and "/cart/" in path:
        item_id = path_parameters.get("itemId") or path.rsplit("/", 1)[-1]
        return _handle_update_item(item_id, event)

    if method == "DELETE" and "/cart/" in path:
        item_id = path_parameters.get("itemId") or path.rsplit("/", 1)[-1]
        return _handle_delete_item(item_id)

    return _response(404, {"message": "Not Found"})
