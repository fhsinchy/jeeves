import click
from click.utils import echo
import docker
from os import path
import json

from docker import client


class Service:
    def __init__(self, tag: str, name: str, image: str, env: dict, volumes: list, ports: dict):
        self.tag = tag
        self.name = name
        self.image = image
        self.env = env
        self.ports = ports
        self.volumes = volumes

def stop_container(container):
    container.stop()
    echo(f"{container.labels['jeeves']} stopped succesfully!")

def remove_container(container):
    container.remove()
    echo(f"{container.labels['jeeves']} removed succesfully!")


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
                ports=service_configuration['ports'],
                volumes=service_configuration['volumes'],
            )

            labels = {
                'jeeves': f"{service.name}--{service.tag}--{service.tag}--{service.ports['destination']}"
            }

            volumes = {
                service.volumes['name']: {
                    'bind': service.volumes['destination'],
                    'mode': 'rw'
                }
            }

            ports = {
                service.ports['source']: service.ports['destination']
            }

            client.containers.run(
                image=f"{service.image}:{service.tag}", environment=service.env, ports=ports, volumes=volumes, labels=labels, detach=True)
        echo(f"{name} started succesfully!")
    else:
        echo(f"{name} is not a valid service name")


@click.command()
@click.option("--all", default=False)
@click.argument('name')
def stop(all, name):
    client = docker.from_env()

    containers = client.containers.list(filters={
        'label': 'jeeves',
        'status': 'running'
    })

    filtered_containers = filter(
        # TODO: find another way of filtering
        lambda container: container.labels['jeeves'].split('--')[0] == name, containers)

    if all:
        for container in filtered_containers:
            stop_container(container)
            remove_container(container)
    else:
        # TODO: make it so that this only shows up if the container count is greater than 1
        for index, container in enumerate(filtered_containers):
            echo(f"{index} --> {container.labels['jeeves']}")
            selected_container = int(input(f"pick the container you want to stop: "))

            stop_container(containers[selected_container])
            remove_container(containers[selected_container])
            


jeeves.add_command(start)
jeeves.add_command(stop)

if __name__ == "__main__":
    jeeves()
