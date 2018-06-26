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

# install Boost.Python
RUN sudo apt-get install -y libboost-python-dev 
RUN sudo apt-get install -y python-dev


