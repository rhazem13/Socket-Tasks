import socket
import tkinter as tk
from tkinter import filedialog, messagebox

class DarkClient:
    def __init__(self):
        self.c_socket = None
        self.host = 'localhost'
        self.port = 5000

        self.window = tk.Tk()
        self.window.title("Dark Client")
        self.window.geometry("500x300")
        self.window.configure(bg="#262626")

        self.select_btn = tk.Button(self.window, text="Select Image", command=self.select_image, bg="#004d99", fg="white", font=("Arial", 16))
        self.select_btn.pack(pady=20)

        self.status_label = tk.Label(self.window, text="Select an image", fg="white", bg="#262626", font=("Arial", 14))
        self.status_label.pack(pady=20)

        self.send_btn = tk.Button(self.window, text="Send Image", command=self.send_image, state=tk.DISABLED, bg="#990000", fg="white", font=("Arial", 16))
        self.send_btn.pack(pady=20)

        self.window.mainloop()

    def select_image(self):
        file_path = filedialog.askopenfilename(initialdir="./", title="Select Image",
                                               filetypes=[("PNG Image", "*.png"),("JPEG Image","*.jpg")])
        if file_path:
            self.file_path = file_path
            self.status_label.config(text=f"Selected image: {file_path}", fg="white", bg="#262626")
            self.send_btn.config(state=tk.NORMAL)

    def send_image(self):
        try:
            self.c_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.c_socket.connect((self.host, self.port))
            filename = self.file_path.split("/")[-1]
            self.c_socket.sendall(filename.encode())
            response = self.c_socket.recv(1024).decode()
            if response == "cancel":
                self.status_label.config(text="Image transfer cancelled", fg="white", bg="#262626")
                return
            with open(self.file_path, "rb") as f:
                while True:
                    data = f.read(1024)
                    if not data:
                        break
                    self.c_socket.sendall(data)
            self.status_label.config(text="Image sent", fg="white", bg="#262626")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to send image: {e}")
        finally:
            if self.c_socket:
                self.c_socket.close()

if __name__ == "__main__":
    dark_client = DarkClient()
