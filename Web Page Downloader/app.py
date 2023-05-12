import tkinter as tk
from tkinter import messagebox
from urllib.parse import urlparse
import requests
import threading
from tkinter.ttk import Progressbar

class WebPageDownloaderGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("600x350")
        self.root.title("Web Page Downloader")
        self.root.config(bg="#212121")

        self.url_label = tk.Label(
            self.root, text="Enter URL:", font=("Arial", 16), fg="white", bg="#212121"
        )
        self.url_label.pack(pady=20)

        self.url_entry = tk.Entry(
            self.root, font=("Arial", 12), width=50, bg="#424242", fg="white"
        )
        self.url_entry.pack(pady=10)

        self.download_button = tk.Button(
            self.root,
            text="Download",
            font=("Arial", 14, "bold"),
            width=20,
            height=2,
            command=self.download_button_clicked,
            bg="#009688",
            fg="white",
            activebackground="#008080",
            activeforeground="white",
        )
        self.download_button.pack(pady=20)

        self.progress_bar = Progressbar(
            self.root,
            orient=tk.HORIZONTAL,
            length=400,
            mode="determinate",
            style="Horizontal.TProgressbar",
        )
        self.progress_bar.pack(pady=10)

        self.root.mainloop()

    def download_button_clicked(self):
        url = self.url_entry.get()
        if not url:
            messagebox.showerror("Error", "Please enter a valid URL.")
            return

        # Check if the URL is valid
        if not self.is_valid_url(url):
            messagebox.showerror("Error", "Invalid URL format.")
            return

        # Start the download in a separate thread
        threading.Thread(target=self.download_web_page, args=(url,)).start()

    def download_web_page(self, url):
        try:
            response = requests.get(url, stream=True, verify=False)
            if response.status_code == 200:
                total_size = int(response.headers.get("Content-Length", 0))
                downloaded_size = 0

                # Save the response to a file
                try:
                    with open("downloaded_page.html", "wb") as file:
                        for chunk in response.iter_content(chunk_size=4096):
                            if chunk:
                                file.write(chunk)
                                downloaded_size += len(chunk)
                                if total_size > 0:
                                    self.update_progress_bar(downloaded_size, total_size)

                    messagebox.showinfo("Success", "Web page downloaded successfully!")
                except Exception as e:
                    messagebox.showerror("Error", f"Error writing file: {e}")
            else:
                messagebox.showerror("Error", f"Request failed with status code: {response.status_code}")
        except requests.RequestException as e:
            messagebox.showerror("Error", f"Error during request: {str(e)}")

    def update_progress_bar(self, downloaded_size, total_size):
        percentage = int((downloaded_size / total_size) * 100)
        self.progress_bar["value"] = percentage
        self.progress_bar.update()

    @staticmethod
    def is_valid_url(url):
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except ValueError:
            return False

if __name__ == "__main__":
    gui = WebPageDownloaderGUI()
