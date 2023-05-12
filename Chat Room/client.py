import socket
import sys
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox

HEADER_LENGTH = 10
IP = "127.0.0.1"
PORT = 1234

# Create the main window
window = tk.Tk()
window.title("Chat Client")
window.configure(bg="#222222")

# Welcome label
welcome_label = tk.Label(window, text="Please Enter Your Name:", bg="#222222", fg="#FFFFFF", font=("Helvetica", 12, "bold"))
welcome_label.pack(padx=10, pady=10)

# Name entry field
name_entry = tk.Entry(window, width=50)
name_entry.pack(padx=10, pady=5)
name_entry.focus()

# Function to send the user's name
def send_name():
    username = name_entry.get()
    if username:
        welcome_label.config(text=f"Hello {username}! You're ready to chat.")
        name_entry.config(state='disabled')
        send_button.config(state='normal')
        message_entry.config(state='normal')
        name_message = f"{username}"
        name_message = name_message.encode('utf-8')
        name_header = f"{len(name_message):<{HEADER_LENGTH}}".encode('utf-8')
        client_socket.send(name_header + name_message)

# Send name button
send_name_button = tk.Button(window, text="Send", command=send_name, bg="#666666", fg="#FFFFFF", font=("Helvetica", 10, "bold"))
send_name_button.pack(pady=5)

# Chat box
chat_box = scrolledtext.ScrolledText(window, width=60, height=20, bg="#333333", fg="#FFFFFF", font=("Helvetica", 10))
chat_box.configure(state="disabled")
chat_box.pack(padx=10, pady=10)

# Function to send a message
def send_message():
    message = message_entry.get()
    if message:
        message = message.encode("utf-8")
        message_header = f"{len(message):<{HEADER_LENGTH}}".encode("utf-8")
        client_socket.send(message_header + message)
        message_entry.delete(0, tk.END)

# Message entry field
message_entry = tk.Entry(window, width=50)
message_entry.pack(padx=10, pady=5)
message_entry.config(state="disabled")

# Send button
send_button = tk.Button(window, text="Send", command=send_message, state="disabled", bg="#666666", fg="#FFFFFF", font=("Helvetica", 10, "bold"))
send_button.pack(pady=5)

# Function to update the chat box with received messages
def update_chat_box(message):
    chat_box.configure(state="normal")
    chat_box.insert(tk.END, message + "\n")
    chat_box.configure(state="disabled")
    chat_box.see(tk.END)

# Function to receive and display messages from the server
def receive_messages(client_socket):
    while True:
        try:
            username_header = client_socket.recv(HEADER_LENGTH)
            if not len(username_header):
                messagebox.showinfo("Disconnected", "Connection closed by the server")
                sys.exit()
            username_length = int(username_header.decode("utf-8").strip())
            username = client_socket.recv(username_length).decode("utf-8")
            message_header = client_socket.recv(HEADER_LENGTH)
            message_length = int(message_header.decode("utf-8").strip())
            message = client_socket.recv(message_length).decode("utf-8")
            update_chat_box(f"{username} > {message}")
        except IOError as e:
            if e.errno != socket.errno.EAGAIN and e.errno != socket.errno.EWOULDBLOCK:
                messagebox.showerror("Reading Error", str(e))
                sys.exit()


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client_socket.connect((IP, PORT))
except ConnectionRefusedError:
    messagebox.showerror("Connection Error", "Failed to connect to the server")
    sys.exit()

receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
receive_thread.start()


def close_window():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        window.destroy()
        sys.exit()


window.protocol("WM_DELETE_WINDOW", close_window)
window.mainloop()
