# openproject-rocketchat
## Requirements

* The latest version of Docker (can be downloaded here: [https://docs.docker.com/engine/installation/](https://docs.docker.com/engine/installation/))
* Docker compose (can be downloaded here: [https://docs.docker.com/compose/install/](https://docs.docker.com/compose/install/))
## Installation

1. Get this repository running the command:

    ```
    git clone https://github.com/sirvantis/openproject-rocketchat/
    ```
2. Edit app.py with your op_project_root_url, rocket_username, rocket_password, rocket_url
2. Create docker image
    ```shell
    docker build -t openproject-rocketchat:1.0
    ```
