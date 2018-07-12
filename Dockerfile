FROM ubuntu:18.04

MAINTAINER Saurav Chhatrapati <sauravc@berkeley.edu> version: 0.1


# run updates
RUN apt-get update

# install version control
RUN apt-get install -y git

# install vim
RUN apt-get install -y vim

# install sudo
RUN apt-get install sudo

# install g++ compiler
RUN sudo apt-get install -y g++

# install Make
RUN sudo apt-get install -y build-essential

# install Boost
RUN sudo apt-get install -y libboost-all-dev

# install Boost.Python
RUN sudo apt-get install -y libboost-python-dev 
RUN sudo apt-get install -y python-dev


# install pip and setup python dependencies
RUN apt install -y python-pip
RUN sudo pip install boto3 cloudpickle Flask Flask-Session pyzmq protobuf requests
COPY . /usr/src/PyBlas

WORKDIR /usr/src/PyBlas

# Compile Boost libraries
RUN ./update.sh
RUN mv build/lib.linux-x86_64-2.7/pyblas.so /usr/src/PyBlas

RUN pip install -r requirements.txt

EXPOSE 6000 

ENTRYPOINT ["python"]

CMD ["server.py"]


