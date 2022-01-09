import json
import click
import docker
from os import path
from docker import client


def stop_container(container):
    container.stop()
    click.echo(f"{container.labels['jeeves']} container stopped succesfully.")


def remove_container(container):
    container.remove()
    click.echo(f"{container.labels['jeeves']} container removed succesfully.")


def get_all_containers(client):
    return client.containers.list(filters={
        'label': 'jeeves',
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
                tag = click.prompt(
                    f"Which tag do you want to use?", type=str, default=service['tag'])
                if tag != '':
                    service['tag'] = tag

                for key, value in service['env'].items():
                    user_input = click.prompt(f"{key}?", type=str, default=value)
                    if user_input != '':
                        service['env'][key] = user_input

                port = click.prompt(
                    f"Which port do you want to use?", type=int, default=service['ports']['destination'])
                if port != '':
                    service['ports']['destination'] = port

                volume = click.prompt(
                    f"What would you like to call your volume?", type=str, default=service['volumes']['name'])
                if volume != '':
                    service['volumes']['name'] = volume

            client = docker.from_env()
            label = f"{service['name']}--{service['tag']}--{service['ports']['destination']}"

            if len(client.containers.list(filters={'label': f"jeeves={label}"})):
                click.echo('container with same attribute is already running.')
            elif len(client.containers.list(filters={'label': f"jeeves={label}", 'status': 'exited'})) > 0:
                click.echo(
                    f"starting previously created {service['name']} container.")
                client.containers.list(
                    filters={'label': f"jeeves={label}", 'status': 'exited'}).pop().start()
            else:
                click.echo(
                    f"creating and starting a new {service['name']} container.")
                client.containers.run(
                    image=f"{service['image']}:{service['tag']}", environment=service['env'], ports={
                        service['ports']['source']: service['ports']['destination']
                    }, volumes={
                        service['volumes']['name']: {
                            'bind': service['volumes']['destination'],
                            'mode': 'rw'
                        }
                    }, labels={
                        'jeeves': label
                    }, command=service['command'], detach=True)
                click.echo(f"{service['name']} started succesfully!")
    else:
        click.echo(f"{name} is not a valid service name.")


@click.command()
@click.option('-a', '--all', default=False, is_flag=True)
@click.argument('name')
def stop(all, name):
    containers = get_all_containers(docker.from_env())

    if len(containers) > 0:
        filtered_containers = tuple(filter(
            lambda container: container.labels['jeeves'].split('--')[0] == name, containers))

        if len(filtered_containers) > 0:
            if all or len(filtered_containers) == 1:
                for container in filtered_containers:
                    stop_container(container)
                    remove_container(container)
            else:
                for index, container in enumerate(filtered_containers):
                    click.echo(f"{index} --> {container.labels['jeeves']}")
                selected_container = click.prompt(
                    f"pick the container you want to stop (0 - {len(filtered_containers) - 1})", type=int)

                stop_container(containers[selected_container])
                remove_container(containers[selected_container])
        else:
            click.echo(f"there are no {name} containers running.")
    else:
        click.echo('there are no containers running.')


@click.command()
def list():
    containers = get_all_containers(docker.from_env())

    click.echo("{:<15} {:<20} {:<20}".format(
        'CONTAINER ID', 'CONTAINER NAME', 'CONTAINER LABEL'))
    for container in containers:
        click.echo("{:<15} {:<20} {:<20}".format(container.short_id,
                                                 container.name, container.labels['jeeves']))


jeeves.add_command(start)
jeeves.add_command(stop)
jeeves.add_command(list)

if __name__ == "__main__":
    jeeves()
