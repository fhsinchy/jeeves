from unicodedata import name
from docker import from_env

client = from_env()

client.containers.create(
    image='docker.io/mysql:latest',
    environment={
        "MYSQL_ROOT_PASSWORD": "root"
    },
    ports={
        '3306/tcp': 3306
    },
    volumes={
        'mysql-data': {
            'bind': '/var/lib/mysql',
            'mode': 'rw'
        }
    },
    name='mysql-dev-server',
    detach=True
)
