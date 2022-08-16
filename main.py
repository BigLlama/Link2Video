from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from pytube import YouTube


root = Tk()
root.title("Link2Video")
root.geometry("600x400")
root.configure(bg="#3a3b3c")
root.iconbitmap("icon.ico")

Grid.rowconfigure(root, [0], weight=2)
Grid.rowconfigure(root, [4], weight=1)
Grid.columnconfigure(root, [0, 1, 2], weight=1)


def get_perc(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage_of_completion = bytes_downloaded / total_size * 100
    perc = int(round(percentage_of_completion, 0))
    barGUI(perc)


def barGUI(perc):
    progressBar = ttk.Progressbar(root, orient=HORIZONTAL, length=300, mode="determinate")
    progressBar.grid(row=4, column=1, sticky="s")

    progressBar["value"] = perc
    root.update_idletasks()


def button():
    # gets link from the entry
    text = link.get()

    # covers the previous "downloaded successfully" and/or "Invalid URL" text
    space = Label(root, bg="#3a3b3c", padx=100)
    space.grid(row=4, column=1)
    download(text)


def download(url):
    chunk_size = 1024
    try:
        video = YouTube(url)
        video.register_on_progress_callback(get_perc)
    except:  # If the URL is invalid
        l = Label(root, text="Invalid URL", bg="#3a3b3c", fg="cyan")
        l.grid(row=4, column=1)
    else:

        # Shows that the video/audio is downloading
        but = Button(root, text="Downloading", relief="raised", bg="#2a3a3f", fg="cyan", command=button)
        but.grid(row=5, column=1, pady=25, sticky="nsew")

        # asks user where to store video/audio
        path = filedialog.askdirectory(title="Choose a download directory")
        location = path
        video = video.streams.get_highest_resolution()
        video.download(location)

        # replaces the download button
        but = Button(root, text="Download Video", relief="raised", bg="#2a3a3f", fg="cyan", command=button)
        but.grid(row=5, column=1, pady=25, sticky="nsew")

        # displays when video has finished downloading
        l = Label(root, text="Video Downloaded Successfully", bg="#3a3b3c", fg="cyan")
        l.grid(row=4, column=1, sticky="nsew")
        l.pack_forget()


# title
title = Label(root, text="Youtube URL To Media Downloader", relief="ridge", bg="#2a3a3f", font=("Arial", 14), borderwidth=7, fg="cyan")
title.grid(row=0, column=0, columnspan=3, sticky="nsew")

# url label
url_entry = Label(root, bg="#3a3b3c", text="Enter url here: ", font=("Arial", 13), fg="white")
url_entry.grid(row=2, column=0, columnspan=3, sticky="nsew")

# link entry
link = Entry(root, relief="sunken", borderwidth=2)
link.grid(row=3, column=1, sticky="nsew")

# download button
but = Button(root, text="Download Video", relief="raised", bg="#2a3a3f", fg="cyan", command=button)
but.grid(row=5, column=1, pady=25, sticky="nsew")


root.mainloop()
