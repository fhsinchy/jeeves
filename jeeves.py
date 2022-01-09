import click
from click.utils import echo
import docker
from os import path
import json

from docker import client


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
@click.option('-d', '--default', default=False, is_flag=True)
@click.argument('name')
def start(default, name):
    if path.exists(f"services/{name}.json"):
        with open(f"services/{name}.json") as f:
            service = json.load(f)

            if not default:
                tag = input(
                    f"Which tag do you want to use? (default: {service['tag']}): ")
                if tag != '':
                    service['tag'] = tag

                for key, value in service['env'].items():
                    user_input = input(f"{key}? (default: {value}): ")
                    if user_input != '':
                        service['env'][key] = user_input

                port = input(
                    f"Which port do you want to use? (default: {service['ports']['destination']}): ")
                if port != '':
                    service['ports']['destination'] = port

                volume = input(
                    f"What would you like to call your volume? (default: {service['volumes']['name']}): ")
                if volume != '':
                    service['volumes']['name'] = volume

            echo(f"starting {service['name']}. hang tight!")
            docker.from_env().containers.run(
                image=f"{service['image']}:{service['tag']}", environment=service['env'], ports={
                    service['ports']['source']: service['ports']['destination']
                }, volumes={
                    service['volumes']['name']: {
                        'bind': service['volumes']['destination'],
                        'mode': 'rw'
                    }
                }, labels={
                    'jeeves': f"{service['name']}--{service['tag']}--{service['ports']['destination']}"
                }, command=service['command'], detach=True)
            echo(f"{service['name']} started succesfully!")
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

    echo("{:<15} {:<20} {:<20}".format(
        'CONTAINER ID', 'CONTAINER NAME', 'CONTAINER LABEL'))
    for container in containers:
        echo("{:<15} {:<20} {:<20}".format(container.short_id,
             container.name, container.labels['jeeves']))


jeeves.add_command(start)
jeeves.add_command(stop)
jeeves.add_command(list)

if __name__ == "__main__":
    jeeves()
