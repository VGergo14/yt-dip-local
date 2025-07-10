import os
import uuid
from flask import Flask, render_template, request, redirect, url_for, flash, send_file
import yt_dlp

app = Flask(__name__)
app.secret_key = str(uuid.uuid4())

# Ensure downloads directory exists
DOWNLOADS_DIR = 'downloads'
if not os.path.exists(DOWNLOADS_DIR):
    os.makedirs(DOWNLOADS_DIR)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download_video():
    video_url = request.form.get('url')
    
    if not video_url:
        flash('Please enter a video URL.', 'error')
        return redirect(url_for('index'))
    
    try:
        # Generate unique filename
        unique_filename = f"{uuid.uuid4()}.mp4"
        output_path = os.path.join(DOWNLOADS_DIR, unique_filename)
        
        # Configure yt-dlp options
        ydl_opts = {
            'outtmpl': output_path,
            'format': 'mp4/best[ext=mp4]',
        }
        
        # Download the video
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        
        # Redirect to download endpoint
        return redirect(url_for('download_file', filename=unique_filename))
        
    except Exception as e:
        flash(f'Error downloading video: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/download/<filename>')
def download_file(filename):
    try:
        file_path = os.path.join(DOWNLOADS_DIR, filename)
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True, download_name=filename)
        else:
            flash('File not found.', 'error')
            return redirect(url_for('index'))
    except Exception as e:
        flash(f'Error serving file: {str(e)}', 'error')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
