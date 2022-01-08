import click
from click.utils import echo
import docker
from os import path
import json

class Service:
    def __init__(self, tag: str, name: str, image: str, env: dict):
        self.tag = tag
        self.name = name
        self.image = image
        self.env = env



@click.group()
def jeeves():
    pass


@click.command()
@click.argument('name')
def start(name):
    client = docker.from_env()

    if path.exists(f"services/{name}.json"):
        with open(f"services/{name}.json") as f:
            service_configuration = json.load(f)

            service = Service(
                tag=service_configuration['tag'],
                name=service_configuration['name'],
                image=service_configuration['image'],
                env=service_configuration['env'],
            )

            client.containers.run(image = f"{service.image}:{service.tag}", environment = service.env, detach=True)
        echo(f"{name} started succesfully!")
    else:
        echo(f"{name} doesn't exist")


jeeves.add_command(start)

if __name__ == "__main__":
    jeeves()
