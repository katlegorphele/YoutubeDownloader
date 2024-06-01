import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from customtkinter import CTk, CTkLabel, CTkEntry, CTkButton, CTkRadioButton, StringVar
import yt_dlp as youtube_dl
import os
from yt_dlp.utils import DownloadError
#from tqdm import tqdm  -- Legacy import. 
import re

class YouTubeDownloader(CTk):
    '''
    * This is a simple YouTube Downloader application that allows you to download videos and playlists from YouTube.
    * The application uses the youtube-dl library to download the videos and playlists.
    '''
    
    def __init__(self):
        super().__init__()

        self.title("YouTube Downloader")
        self.geometry("600x500")
        self.configure(bg="black")

        # Link input
        self.link_label = CTkLabel(self, text="YouTube Link:")
        self.link_label.pack(pady=10)
        self.link_entry = CTkEntry(self, width=500)
        self.link_entry.pack(pady=5)

        # Resolution input
        self.resolution_label = CTkLabel(self, text="Resolution:")
        self.resolution_label.pack(pady=10)
        
        self.resolution_var = StringVar(value="720p")
        
        self.resolution_frame = tk.Frame(self)
        self.resolution_frame.pack(pady=5)

        self.resolution_720p_button = CTkRadioButton(self.resolution_frame, text="720p", variable=self.resolution_var, value="720p")
        self.resolution_720p_button.pack(side=tk.LEFT, padx=10)

        self.resolution_1080p_button = CTkRadioButton(self.resolution_frame, text="1080p", variable=self.resolution_var, value="1080p")
        self.resolution_1080p_button.pack(side=tk.LEFT, padx=10)

        # Destination folder input
        self.destination_label = CTkLabel(self, text="Destination Folder:")
        self.destination_label.pack(pady=10)
        self.destination_button = CTkButton(self, text="Select Folder", command=self.select_folder)
        self.destination_button.pack(pady=5)
        self.destination_entry = CTkEntry(self, width=500)
        self.destination_entry.pack(pady=5)

        # Download button
        self.download_button = CTkButton(self, text="Download Video", command=self.download_video)
        self.download_button.pack(pady=20)

        # Download playlist button
        self.download_playlist_button = CTkButton(self, text="Download Playlist", command=self.download_playlist)
        self.download_playlist_button.pack(pady=20)

        # Progress bar
        self.progress = ttk.Progressbar(self, orient=tk.HORIZONTAL, length=100, mode='determinate')
        self.progress.pack(pady=20)

    def select_folder(self):
        '''
        Opens a dialog to select destination folder.
        '''
        folder = filedialog.askdirectory()
        self.destination_entry.delete(0, tk.END)
        self.destination_entry.insert(0, folder)

    def get_inputs(self):
        '''
        Get the inputs from the entry fields and radio buttons.
        If any field is empty, show an error message and return None.
        Otherwise, return a tuple of the inputs.
        '''
        link = self.link_entry.get()
        resolution = self.resolution_var.get()
        destination = self.destination_entry.get()

        if not link or not resolution or not destination:
            messagebox.showerror("Error", "Please fill in all fields.")
            return None

        return link, resolution, destination

    def download(self, link, resolution, destination, outtmpl):
        '''
        Download a video or playlist from YouTube with the given link, resolution, and destination.
        If the download fails, show an error message and return False.
        Otherwise, return True.
        '''
        ydl_opts = {
            'format': f'best[height<={resolution[:-1]}]',
            'outtmpl': os.path.join(destination, outtmpl),
            'noplaylist': True,
            'progress_hooks': [self.my_hook],
        }

        try:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([link])
            return True
        except DownloadError as e:
            messagebox.showerror("Error", f"Failed to download: {e}")
            return False
        
    def my_hook(self, d):
        '''
        Update the progress bar with the current download progress.
        '''
        if d['status'] == 'downloading':
            percent_str = re.sub(r'\x1b\[.*?m', '', d['_percent_str'])
            self.progress['value'] = int(float(percent_str.replace('%','')))
        if d['status'] == 'finished':
            print('Done downloading')

    def download_video(self):
        '''
        Get the inputs and download a video from YouTube.
        If the download is successful, show a success message.
        '''
        inputs = self.get_inputs()
        if inputs is None:
            return

        link, resolution, destination = inputs
        if self.download(link, resolution, destination, '%(title)s.%(ext)s'):
            messagebox.showinfo("Success", "Video downloaded successfully!")

    def download_playlist(self):
        '''
        Get the inputs and download a playlist from YouTube.
        If the download is successful, show a success message.
        '''
        inputs = self.get_inputs()
        if inputs is None:
            return

        link, resolution, destination = inputs
        if self.download(link, resolution, destination, '%(playlist)s/%(title)s.%(ext)s'):
            messagebox.showinfo("Success", "Playlist downloaded successfully!")

if __name__ == "__main__":
    app = YouTubeDownloader()
    app.mainloop()