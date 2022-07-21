#!/bin/bash

sudo apt update

sudo apt install apt-transport-https ca-certificates curl software-properties-common

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable"

apt-cache policy docker-ce

sudo apt install docker-ce

sudo usermod -aG docker ${whoami}


echo -e 'GOOD JOB....DOCKER IS DONE!! \n TO SEE DOCKER STATUS => sudo systemctl status docker'
echo 'Installing docker-compose......'

sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
docker–compose --version

echo '<<<<< END SCRIPT....>>>>>'
