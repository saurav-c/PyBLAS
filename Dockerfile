FROM ubuntu:18.04

MAINTAINER Saurav Chhatrapati <sauravc@berkeley.edu> version: 0.1


# run updates
RUN apt-get update

# install version control
RUN apt-get install -y git

# install vim
RUN apt-get install -y vim
