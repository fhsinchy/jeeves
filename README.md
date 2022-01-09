# Jeeves

Jeeves is a CLI tool for running development dependencies such as MySQL, Mongo, Redis etc inside pre-configured containers using simple one-liners.

Running containers can be accessed via their exposed ports and can be paired with any other application on your system.

Starting a service such as `mysql` is as simple as executing `jeeves start mysql` and you'll never have to look back at it.

But `mysql` is not the only available service. A list of all the available services can be found on the [services](https://github.com/fhsinchy/jeeves/tree/master/services) directory

Jeeves is heavily inspired from [tighten/takeout](https://github.com/tighten/takeout) and [fhsinchy/tent](https://github.com/fhsinchy/tent) projects. It is an experimental project. Hence, care should be taken if you're using it in a critical environment.

## Requirements

- Python 3
- Docker

## Installation

```shell
pip install git+https://github.com/fhsinchy/jeeves.git#egg=jeeves
pip freeze
```

Output &ndash;

```shell
jeeves==<version number>
```

## Usage

The `jeeves` program has following commands:

* `jeeves start <service name>` - starts a container for the given service
* `jeeves stop <service name>` - stops and removes a container for the given service
* `jeeves list` - lists all running containers

All the services in `jeeves` utilizes volumes for persisting data, so even if you stop a service, it's data will be persisted in a volume for later usage. These volumes can listed by executing `docker volume ls` and can be managed like any other Docker volume.

### Start a Service

The generic syntax for the `start` command is as follows:

```bash
jeeves start <service name>

## starts mysql and prompts you where necessary
jeeves start mysql
```

### Start Service with Default Configuration

The `--default` flag for the `start` command can be used to skip all the prompts and start a service with default configuration

```bash
jeeves start <service name> --default

## starts mysql with the default configuration
jeeves start mysql --default
```

### Stop a Service

The generic syntax for the `stop` command is as follows:

```bash
jeeves stop <service name>

## stops mysql and removes the container
## prompts you if multiple containers are found
jeeves stop mysql

## stops all mysql containers and removes them
jeeves stop mysql --all
```

## Running Multiple Versions

Given all the services are running inside containers, you can spin up multiple versions of the same service as long as you're keeping the port different.

Run `jeeves start mysql` twice; the first time, use the `--default` flag, and the second time, put `5.7` as tag and `3307` as host port.

Now, if you run `jeeves list`, you'll see both services running at the same time.

```bash
CONTAINER ID    CONTAINER NAME       CONTAINER LABEL     
e26c7f47e6      priceless_euler      mysql--5.7--3308    
6cc3f50081      interesting_ptolemy  mysql--latest--3306
```

## Container Management

Containers started by `jeeves` are regular containers with some pre-set configurations. So you can use regular `docker` commands such as `ls`, `inspect`, `logs` etc on them. Although `jeeves` comes with a `list` command, using the `docker` commands will result in more informative results. The target of `jeeves` is to provide plug and play containers, not to become a full-fledged `docker` cli.
