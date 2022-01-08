import click
import docker

@click.group()
def main():
    pass

@click.command()
def hello():
    client = docker.from_env()

    print(client.containers.run('busybox', "echo Hello World!"))

main.add_command(hello)

if __name__ == "__main__":
    main()
