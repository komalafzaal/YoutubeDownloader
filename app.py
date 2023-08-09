from flask import Flask, render_template, request, send_file
from pytube import YouTube

app = Flask(__name__)

@app.route('/')
def main():
    return render_template("youtube.html")

@app.route('/videoDownload', methods=["POST", "GET"])
def videoDownload():
    try:
        if request.method == "POST":
            l = request.form["link"]
        else:
            l = request.args.get("link")

        youtube = YouTube(l)
        vid = youtube.streams.filter(progressive=True, file_extension='mp4').get_highest_resolution().download()
        fname = vid.split("/")[-1]
        return send_file(fname, as_attachment=True)
    except:
        return "Video download failed!"

@app.route('/audio')
def audio():
    return render_template("youtubeaudio.html")

@app.route('/audioDownload', methods=["POST", "GET"])
def audioDownload():
    try:
        if request.method == "POST":
            l = request.form["link"]
        else:
            l = request.args.get("link")

        youtube = YouTube(l)
        audio_stream = youtube.streams.filter(only_audio=True).first()
        audio_stream.download(filename='audio')  # Save with a specific filename
        return "Audio downloaded successfully!"
    except:
        return "Audio download failed!"


if __name__ == '__main__':
    app.run(debug=True)
