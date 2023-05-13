import socket
import threading
import tkinter as tk
from tkinter import messagebox

class ServerGUI:
    def __init__(self):
        self.server_socket = None
        self.client_socket = None
        self.receive_thread = None
        self.host = 'localhost'
        self.port = 5000
        self.connected = False

        self.root = tk.Tk()
        self.root.title("File Receiver")
        self.root.geometry("500x250")
        self.root.configure(bg="#2c3e50")

        self.start_button = tk.Button(self.root, text="Start Server", command=self.start_server, bg="#3498db", fg="white", padx=20, pady=10, font=("Arial", 12))
        self.start_button.pack(pady=20)

        self.stop_button = tk.Button(self.root, text="Stop Server", command=self.stop_server, state=tk.DISABLED, bg="#e74c3c", fg="white", padx=20, pady=10, font=("Arial", 12))
        self.stop_button.pack(pady=10)

        self.status_label = tk.Label(self.root, text="Not Running", fg="white", bg="#2c3e50", font=("Arial", 14))
        self.status_label.pack(pady=10)

        self.root.mainloop()

    def start_server(self):
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

        self.server_thread = threading.Thread(target=self.start_server_thread)
        self.server_thread.start()

    def start_server_thread(self):
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(1)
            self.connected = True
            self.status_label.config(text=f"Server running on {self.host}:{self.port}")
            while self.connected:
                self.client_socket, client_address = self.server_socket.accept()
                self.receive_thread = threading.Thread(target=self.receive_file, args=(self.client_socket,))
                self.receive_thread.start()
        except Exception as e:
            self.status_label.config(text=f"Error: {e}")
            self.stop_server()

    def stop_server(self):
        self.connected = False
        if self.client_socket:
            self.client_socket.close()
        if self.server_socket:
            self.server_socket.close()
        if self.receive_thread and self.receive_thread.is_alive():
            self.receive_thread.join()
        self.status_label.config(text="Not Running")
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

    def receive_file(self, client_socket):
        try:
            filename = client_socket.recv(1024).decode()
            save_path = f"./received_files/{filename}"  # Change the save path as needed
            client_socket.sendall(b"ok")
            with open(save_path, 'wb') as f:
                while True:
                    data = client_socket.recv(1024)
                    if not data:
                        break
                    f.write(data)
            messagebox.showinfo("File Transfer", f"{filename} received successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    ServerGUI()
