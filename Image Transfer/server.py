import socket
import threading
import tkinter as tk
from tkinter import filedialog, messagebox

class FancyServer:
    def __init__(self):
        self.server_socket = None
        self.client_socket = None
        self.receive_thread = None
        self.host = 'localhost'
        self.port = 5000
        self.connected = False

        self.root = tk.Tk()
        self.root.title("Fancy Server")
        self.root.geometry("500x300")
        self.root.configure(bg="#262626")

        self.start_btn = tk.Button(self.root, text="Start Server", command=self.start_server, bg="#004d99", fg="white", font=("Arial", 16))
        self.start_btn.pack(pady=20)

        self.stop_btn = tk.Button(self.root, text="Stop Server", command=self.stop_server, state=tk.DISABLED, bg="#990000", fg="white", font=("Arial", 16))
        self.stop_btn.pack(pady=20)

        self.status_label = tk.Label(self.root, text="Not Running", fg="white", bg="#262626", font=("Arial", 14))
        self.status_label.pack(pady=20)

        self.root.mainloop()

    def start_server(self):
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)

        self.server_thread = threading.Thread(target=self.start_server_thread)
        self.server_thread.start()

    def start_server_thread(self):
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(1)
            self.connected = True
            self.status_label.config(text=f"Server running on {self.host}:{self.port}", fg="white", bg="#262626")
            while self.connected:
                self.client_socket, client_address = self.server_socket.accept()
                self.receive_thread = threading.Thread(target=self.receive_image, args=(self.client_socket,))
                self.receive_thread.start()
        except Exception as e:
            self.status_label.config(text=f"Error: {e}", fg="white", bg="#262626")
            self.stop_server()

    def stop_server(self):
        self.connected = False
        if self.client_socket:
            self.client_socket.close()
        if self.server_socket:
            self.server_socket.close()
        if self.receive_thread and self.receive_thread.is_alive():
            self.receive_thread.join()
        self.status_label.config(text="Not Running", fg="white", bg="#262626")
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)

    def receive_image(self, client_socket):
        try:
            filename = client_socket.recv(1024).decode()
            save_path = filedialog.asksaveasfilename(initialdir="./", title="Save Image As", initialfile=filename,
                                                     filetypes=[("PNG Image", "*.png"),("JPEG Image","*.jpg")])
            if not save_path:
                client_socket.sendall(b"cancel")
                return
            client_socket.sendall(b"ok")
            with open(save_path, "wb") as f:
                while True:
                    data = client_socket.recv(1024)
                    if not data:
                        break
                    f.write(data)
            self.status_label.config(text=f"Image received and saved as {save_path}", fg="white", bg="#262626")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to receive image: {e}")
        finally:
            client_socket.close()

if __name__ == "__main__":
    dark_server = FancyServer()
