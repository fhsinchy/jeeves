import click
from click.utils import echo
import docker
from os import path
import json

from docker import client


class Service:
    def __init__(self, tag: str, name: str, image: str, env: dict, volumes: list, ports: dict, command: str):
        self.tag = tag
        self.name = name
        self.image = image
        self.env = env
        self.ports = ports
        self.volumes = volumes
        self.command = command

def stop_container(container):
    container.stop()
    echo(f"{container.labels['jeeves']} stopped succesfully!")

def remove_container(container):
    container.remove()
    echo(f"{container.labels['jeeves']} removed succesfully!")

def get_all_running_containers(client):
    return client.containers.list(filters={
        'label': 'jeeves',
        'status': 'running'
    })


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
                command=service_configuration['command'],
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

            echo(f"starting {name}. hang tight!")
            client.containers.run(
                image=f"{service.image}:{service.tag}", environment=service.env, ports=ports, volumes=volumes, labels=labels, command=service.command, detach=True)
            echo(f"{name} started succesfully!")
    else:
        echo(f"{name} is not a valid service name")


@click.command()
@click.argument('name')
def stop(name):
    containers = get_all_running_containers(docker.from_env())

    filtered_containers = tuple(filter(lambda container: container.labels['jeeves'].split('--')[0] == name, containers))

    if len(filtered_containers) > 1:
        for index, container in enumerate(filtered_containers):
            echo(f"{index} --> {container.labels['jeeves']}")
            selected_container = int(input(f"pick the container you want to stop (0 - {len(filtered_containers) - 1}): "))

            stop_container(containers[selected_container])
            remove_container(containers[selected_container])
    else:
        for container in filtered_containers:
            stop_container(container)
            remove_container(container)
            

@click.command()
def list():
    containers = get_all_running_containers(docker.from_env())

    for container in containers:
        echo(container.labels['jeeves'])



jeeves.add_command(start)
jeeves.add_command(stop)
jeeves.add_command(list)

if __name__ == "__main__":
    jeeves()
