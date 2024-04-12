import os
import requests
from tkinter import Tk, Label, Entry, Button, messagebox, filedialog, Toplevel
from tkinter.constants import INSERT
from plyer import notification
from pytube import YouTube

def download_image(image_url, path, filename):
    full_path = os.path.join(path, filename + '.jpg')
    if os.path.exists(full_path):
        replace = messagebox.askyesno("Файл существует", "Файл уже существует. Заменить?")
        if not replace:
            i = 1
            while os.path.exists(os.path.join(path, f'{filename}_{i}.jpg')):
                i += 1
            full_path = os.path.join(path, f'{filename}_{i}.jpg')
    img_data = requests.get(image_url).content
    with open(full_path, 'wb') as handler:
        handler.write(img_data)
    notification.notify(
        title="MediaMagnet",
        message="Превью загружено",
        timeout=10
    )

def youtube(url):
    yt = YouTube(url)
    image_url = yt.thumbnail_url
    path = filedialog.askdirectory()
    if path:
     download_image(image_url, path, 'preview')

def downloadYouTube(videourl, path , video_quality):
    try:
        notification.notify(
            title="MediaMagnet",
            message="Идет загрузка видео...",
            timeout=10
        )
        yt = YouTube(videourl)
        yt = yt.streams.filter(res=video_quality).order_by('resolution').first()
        base = os.path.join(path, yt.title)
        new_file = base + '.mp4'
        if os.path.exists(new_file):
            replace = messagebox.askyesno("Файл существует", "Файл уже существует. Заменить?")
            if replace:
                os.remove(new_file)  # Удалите существующий файл перед загрузкой
            else:
                i = 1
                while os.path.exists(base + f'_{i}.mp4'):
                    i += 1
                new_file = base + f'_{i}.mp4'
        out_file = yt.download(path, filename=new_file)  # Загрузите файл с новым именем
        os.rename(out_file, new_file)
        notification.notify(
            title="MediaMagnet",
            message="Видео загружено",
            timeout=10
        )
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось загрузить файл из-за ошибки: {str(e)}")

def downloadAudioFromYoutube(videourl, path):
    try:
        yt = YouTube(videourl)
        video = yt.streams.filter(only_audio=True).first()

        base = os.path.join(path, video.title)
        new_file = base + '.mp3'
        if os.path.exists(new_file):
            replace = messagebox.askyesno("Файл существует", "Файл уже существует. Заменить?")
            if replace:
                os.remove(new_file)  # Удалите существующий файл перед загрузкой
            else:
                i = 1
                while os.path.exists(base + f'_{i}.mp3'):
                    i += 1
                new_file = base + f'_{i}.mp3'
        out_file = video.download(output_path=path, filename=new_file)  # Загрузите файл с новым именем
        os.rename(out_file, new_file)
        notification.notify(
            title="MediaMagnet",
            message="Аудио загружено",
            timeout=10
        )
    except Exception as e:
        messagebox.showerror("Ошибка", f"Ошибка: {str(e)}")



def Main():
    root = Tk()
    root.title("MediaMagnet")
    Label(root, text="Введите ссылку на видео:").pack()
    url_entry = Entry(root, width=50)
    url_entry.pack()
    url_entry.bind('<Control-igrave>', lambda event: url_entry.insert(INSERT, root.clipboard_get()))  # Изменено здесь
    Button(root, text="Вставить из буфера обмена", command=lambda: url_entry.insert(0, root.clipboard_get())).pack()
    Label(root, text="Выберите действие:").pack()
    Button(root, text="Скачать превью", command=lambda: youtube(url_entry.get())).pack()
    Button(root, text="Скачать видео", command=lambda: selectQuality(root, url_entry.get())).pack()
    Button(root, text="Скачать аудио", command=lambda: downloadAudio(root, url_entry.get())).pack()
    root.mainloop()


def selectQuality(root, videourl):
    qualityWindow = Toplevel(root)
    qualityWindow.geometry("+%d+%d" % (root.winfo_rootx(), root.winfo_rooty()))  # Окно появляется рядом с основным окном
    qualityWindow.title("Выберите качество видео")
    Button(qualityWindow, text="240p", command=lambda: downloadAndClose(qualityWindow, videourl, "240p")).pack()
    Button(qualityWindow, text="360p", command=lambda: downloadAndClose(qualityWindow, videourl, "360p")).pack()
    Button(qualityWindow, text="480p", command=lambda: downloadAndClose(qualityWindow, videourl, "480p")).pack()
    Button(qualityWindow, text="720p", command=lambda: downloadAndClose(qualityWindow, videourl, "720p")).pack()

def downloadAndClose(window, videourl, quality):
    path = filedialog.askdirectory()
    if path:
        downloadYouTube(videourl, path, quality)
        window.destroy()

def downloadAudio(root, videourl):
    path = filedialog.askdirectory()
    if path:
        downloadAudioFromYoutube(videourl, path)

if __name__ == "__main__":
    Main()
