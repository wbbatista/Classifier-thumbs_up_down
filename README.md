# CNN Image Classifier thumbsup | tumbsdown
* On Linux Ubuntu 18.04
* With keras and Tensorflow

 
# Files
* amostras_para_testes <b>-</b> 20 image samples 
* st_images <b>-</b> used images in the streamlit app layout
* Dockfile <b>-</b> instructions to build a docker image
* app.mp4 <b>-</b> video running the application 
* app.py <b>-</b> main file
* exercicio1 <b>-</b> answers of exercise 1
* requiriments.txt <b>-</b> all dependencies
* resources.zip <b>-</b> Treined model

# Install Docker

* [Docker Install](https://docs.docker.com/engine/install/ubuntu/)

# unzip resources.zip, 
unzip resources.zip

* if you do not have it installed, run: sudo apt-get install unzip
# create an image
sudo docker build --tag demo_app .

# run image as a container
sudo docker run -p 8501:8501 --privileged -v /dev/video0:/dev/video0  demo_app

# only if you need to stop the running process
sudo docker rm --force demo_app

# only if you need to remove image
sudo docker image rm -f demo_app

# only if you need to remove all dockers
* sudo docker rm -vf $(sudo docker ps -a -q)
* sudo docker rmi -f $(sudo docker images -a -q)
* sudo docker system prune -a --volumes



