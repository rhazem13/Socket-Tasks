# Socket-Tasks Repository

This repository contains four projects implemented using Sockets in Python.

## Chat Room

The Chat Room project is a simple client-server application that allows multiple users to communicate in real-time. It provides a chat interface where users can send and receive messages. The server manages the connections between clients and relays the messages.

## File Transfer

The File Transfer project enables the transfer of files between a client and a server. The client can select a file from their local machine and send it to the server. The server receives the file and saves it locally.

## Image Transfer

The Image Transfer project focuses on sending images between a client and a server. The client can choose an image file, and the server receives and saves the image. It supports popular image formats such as PNG and JPEG.

## Web Page Downloader

The Web Page Downloader project allows the user to download the HTML content of a web page given its URL. It utilizes the `urllib` library to make an HTTP request to the specified URL and saves the HTML response to a local file.

## Requirements

- Python 3.x

## Usage

Each project is contained within its respective directory. To run a project, navigate to its directory and execute the main Python file.

For example, to run the Chat Room project:

```shell
cd chat-room/
python server.py  # Run the server
python client.py  # Run the client
