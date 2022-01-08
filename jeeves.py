import docker

def main():
    client = docker.from_env()

    print(client.containers.run('busybox', "echo Hello World!"))

if __name__ == "__main__":
    main()