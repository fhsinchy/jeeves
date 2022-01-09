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

    def ask_questions(self):
        tag = input(f"Which tag do you want to use? (default: {self.tag}): ")
        if tag != '':
            self.tag = tag

        for key, value in self.env.items():
            user_input = input(f"{key}? (default: {value}): ")
            if user_input != '':
                self.env[key] = user_input

        port = input(
            f"Which port do you want to use? (default: {self.ports['destination']}): ")
        if port != '':
            self.ports['destination'] = port

        volume = input(
            f"What would you like to call your volume? (default: {self.volumes['name']}): ")
        if volume != '':
            self.volumes['name'] = volume

    def start_container(self):
        self.ask_questions()
        echo(f"starting {self.name}. hang tight!")
        docker.from_env().containers.run(
            image=f"{self.image}:{self.tag}", environment=self.env, ports={
                self.ports['source']: self.ports['destination']
            }, volumes={
                self.volumes['name']: {
                    'bind': self.volumes['destination'],
                    'mode': 'rw'
                }
            }, labels={
                'jeeves': f"{self.name}--{self.tag}--{self.ports['destination']}"
            }, command=self.command, detach=True)
        echo(f"{self.name} started succesfully!")


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

            service.start_container()
    else:
        echo(f"{name} is not a valid service name")


@click.command()
@click.argument('name')
def stop(name):
    containers = get_all_running_containers(docker.from_env())

    filtered_containers = tuple(filter(
        lambda container: container.labels['jeeves'].split('--')[0] == name, containers))

    if len(filtered_containers) > 1:
        for index, container in enumerate(filtered_containers):
            echo(f"{index} --> {container.labels['jeeves']}")
        selected_container = int(input(
            f"pick the container you want to stop (0 - {len(filtered_containers) - 1}): "))

        stop_container(containers[selected_container])
        remove_container(containers[selected_container])
    else:
        for container in filtered_containers:
            stop_container(container)
            remove_container(container)


@click.command()
def list():
    containers = get_all_running_containers(docker.from_env())

    echo("{:<15} {:<20} {:<20}".format('CONTAINER ID','CONTAINER NAME','CONTAINER LABEL'))
    for container in containers:
        echo("{:<15} {:<20} {:<20}".format(container.short_id, container.name, container.labels['jeeves']))


jeeves.add_command(start)
jeeves.add_command(stop)
jeeves.add_command(list)

if __name__ == "__main__":
    jeeves()
