import typer
import random
import string


def add_server_to_ddb_inventory_table(server_name: str):
    print(
        f"Adding '{server_name}' to DynamoDB inventory table.")

    # Add new code here


def _generate_server_name():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))


def main():
    name = _generate_server_name()
    add_server_to_ddb_inventory_table(name)
    print(f"Generated server name: {name}")


if __name__ == "__main__":
    typer.run(main)
