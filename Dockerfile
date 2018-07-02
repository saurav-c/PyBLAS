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

# Setup repo
RUN cd usr/src && git clone https://github.com/saurav-c/PyBLAS.git

# install pip and setup python dependencies
RUN apt install -y python-pip
RUN sudo pip install boto3 cloudpickle Flask Flask-Session pyzmq protobuf requests



