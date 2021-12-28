import docker
client = docker.from_env()

print(client.containers.run('busybox', "echo Hello World!"))