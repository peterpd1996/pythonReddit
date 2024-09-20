import os
import subprocess
from pydub import AudioSegment
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, AudioFileClip, CompositeAudioClip
import moviepy.editor as mpe
# Hàm chia nhỏ văn bản thành các cặp từ
def split_text_into_pairs(text):
    words = text.split()
    pairs = [" ".join(words[i:i + 2]) for i in range(0, len(words), 2)]
    return pairs

# Hàm tạo file phụ đề SRT
def create_srt_file(pairs, srt_file, audio_duration):
    interval_per_pair = audio_duration / len(pairs)  # Thời gian hiển thị mỗi cặp từ

    with open(srt_file, 'w') as f:
        for index, pair in enumerate(pairs):
            start_time = index * interval_per_pair
            end_time = start_time + interval_per_pair
            f.write(f"{index + 1}\n")
            f.write(f"{format_time(start_time)} --> {format_time(end_time)}\n")
            f.write(pair + "\n\n")

# Hàm định dạng thời gian thành dạng SRT (giờ:phút:giây,miligiây)
def format_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 1000)
    return f"{hours:02}:{minutes:02}:{secs:02},{millis:03}"

# Hàm thêm phụ đề vào video bằng ffmpeg
def overlay_captions(video_file, srt_file, output_video_file):
    subprocess.run([
        "ffmpeg", "-i", video_file, "-vf", f"subtitles={srt_file}",
        output_video_file
    ])

# Hàm thêm âm thanh vào video bằng ffmpeg
def add_audio_to_video(video_file, audio_file, output_video_file):
    process = subprocess.run([
        "ffmpeg", "-i", video_file, "-i", audio_file, "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-shortest", output_video_file
    ], stderr=subprocess.PIPE)

    # Kiểm tra lỗi ffmpeg nếu quá trình không thành công
    if process.returncode != 0:
        print("Error adding audio to video:")
        print(process.stderr.decode('utf-8'))

# Hàm thực hiện quá trình thêm phụ đề và âm thanh vào video
def process_with_captions_and_audio(video_file, audio_file, text, output_video_with_audio_and_sub):
    # Bước 1: Chia văn bản thành từng cặp từ
    pairs = split_text_into_pairs(text)
    
    # Lấy thời lượng của file âm thanh
    audio = AudioSegment.from_file(audio_file)
    audio_duration = len(audio) / 1000  # Đổi sang giây

    # Bước 2: Tạo file SRT cho phụ đề với mỗi lần hiển thị 2 từ
    srt_file = "output_captions.srt"
    create_srt_file(pairs, srt_file, audio_duration)
    
    # Bước 3: Thêm âm thanh vào video
    video_with_audio = "temp_video_with_audio.mp4"
    add_audio_to_video(video_file, audio_file, video_with_audio)
    
    # Bước 4: Thêm phụ đề vào video (sau khi đã thêm âm thanh)
    overlay_captions(video_with_audio, srt_file, output_video_with_audio_and_sub)
    
    # Xóa file tạm
    os.remove(video_with_audio)


def add_audio_to_video2(fileVideo, fileMp3):
    # Đọc file audio từ MP3
    audio = AudioFileClip(fileMp3)
    
    # Đọc file video từ MP4
    video1 = VideoFileClip(fileVideo)
    
    # Gán âm thanh cho video
    final = video1.set_audio(audio)
    
    # Xuất video với âm thanh mới
    final.write_videofile("audio_video_ok.mp4", codec="libx264", audio_codec="aac")

# Gọi hàm để thêm âm thanh vào video
fileVideo = "your_video.mp4"  # Đường dẫn đến file video
fileMp3 = "your_audio.mp3"    # Đường dẫn đến file âm thanh

# Thực hiện toàn bộ quy trình
video_file = "input_video.mp4"  # File video đầu vào chưa có âm thanh
audio_file = "audio1.mp3"
output_video_with_audio_and_sub = "output_video_with_audio_and_sub.mp4"  # Video đầu ra đã có âm thanh và phụ đề
text = "In a quiet village where the sky brushes the fields in hues of gold, young Mia discovered a map leading to forgotten treasures. Little did she know, her cat Whiskers had a secret: he was the guardian of the map, tasked with guiding Mia to not only the treasure but also to her destiny."  # Đặt văn bản của bạn ở đây

# process_with_captions_and_audio(video_file, audio_file, text, output_video_with_audio_and_sub)


#add_audio_to_video(video_file, audio_file, 'video_audio1.mp4')

add_audio_to_video2(video_file, audio_file)

