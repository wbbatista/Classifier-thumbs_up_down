# CNN Image Classifier thumbsup | tumbsdown
* On Linux Ubuntu 18.04

 
# Files
* amostras_para_testes - 20 image samples 
* st_images - images used on layout app streamlit
* Dockfile - instructions to build a container image
* app.mp4 - video exemplo running the aplication 
* app.py - main file
* exercicio1 - answers of exercicio1
* requiriments.txt - all dependencies

# ---------------------------------------------------------------------------
# Install Docker

* [Docker Install](https://docs.docker.com/engine/install/ubuntu/)

# unzip resources.zip, Treined model with keras and Tensorflow
unzip resources.zip

* if you do not have it installed, run: sudo apt-get install unzip
# create an image
sudo docker build --tag demo_app .

# run image as a container
sudo docker run -p 8501:8501 --privileged -v /dev/video0:/dev/video0  demo_app

# stop process
sudo docker rm --force demo_app

# if you need to remove image
sudo docker image rm -f demo_app

# to remove all dockers
* sudo docker rm -vf $(sudo docker ps -a -q)
* sudo docker rmi -f $(sudo docker images -a -q)
* sudo docker system prune -a --volumes



