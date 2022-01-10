services = {
    "mariadb": {
        "name": "mariadb",
        "image": "docker.io/mariadb",
        "tag": "latest",
        "env": {
            "MYSQL_ROOT_PASSWORD": "root"
        },
        "ports": {
            "source": "3306/tcp",
            "destination": 3306
        },
        "volumes": {
            "name": "mariadb-data",
            "destination": "/var/lib/mysql"
        },
        "command": ""
    },
    "mongo": {
        "name": "mongo",
        "image": "docker.io/mongo",
        "tag": "latest",
        "env": {
            "MONGO_INITDB_ROOT_USERNAME": "admin",
            "MONGO_INITDB_ROOT_PASSWORD": "admin"
        },
        "ports": {
            "source": "27017/tcp",
            "destination": 27017
        },
        "volumes": {
            "name": "mongo-data",
            "destination": "/data/db"
        },
        "command": "--serviceExecutor adaptive"
    },
    "mysql": {
        "name": "mysql",
        "image": "docker.io/mysql",
        "tag": "latest",
        "env": {
            "MYSQL_ROOT_PASSWORD": "root"
        },
        "ports": {
            "source": "3306/tcp",
            "destination": 3306
        },
        "volumes": {
            "name": "mysql-data",
            "destination": "/var/lib/mysql"
        },
        "command": ""
    },
    "postgres": {
        "name": "postgres",
        "image": "docker.io/postgres",
        "tag": "latest",
        "env": {
            "POSTGRES_PASSWORD": "postgres"
        },
        "ports": {
            "source": "5432/tcp",
            "destination": 5432
        },
        "volumes": {
            "name": "postgres-data",
            "destination": "/var/lib/postgresql/data"
        },
        "command": ""
    },
    "redis": {
        "name": "redis",
        "image": "docker.io/redis",
        "tag": "latest",
        "env": {},
        "ports": {
            "source": "6379/tcp",
            "destination": 6379
        },
        "volumes": {
            "name": "redis-data",
            "destination": "/data"
        },
        "command": ""
    }
}
