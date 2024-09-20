import random
from moviepy.editor import VideoFileClip, AudioFileClip
import os
import sys

def split_text(text):
    words = text.split()
    chunks = []
    i = 0

    # Chia đoạn text thành các chunk có 2-3 từ mỗi chunk
    while i < len(words):
        words_per_chunk = random.randint(2, 3)
        chunk = " ".join(words[i:i + words_per_chunk])
        chunks.append(chunk)
        i += words_per_chunk

    return chunks

def calculate_duration_per_chunk(text_chunks, total_duration, words_per_second=2.5):
    """
    Tính toán thời gian hiển thị cho từng đoạn text dựa trên số từ và tổng thời lượng audio.
    Mặc định là 2.5 từ/giây.
    """
    total_words = sum(len(chunk.split()) for chunk in text_chunks)  # Tổng số từ
    durations = []

    # Tính thời gian cho từng chunk dựa trên số từ
    for chunk in text_chunks:
        words_in_chunk = len(chunk.split())
        chunk_duration = words_in_chunk / words_per_second
        durations.append(chunk_duration)

    # Chuẩn hóa thời gian để đảm bảo tổng thời lượng bằng với thời lượng âm thanh
    scale_factor = total_duration / sum(durations)
    durations = [d * scale_factor for d in durations]

    return durations

def create_srt_file(text_chunks, chunk_durations, srt_filename):
    """
    Tạo file SRT từ các đoạn text và thời gian hiển thị.
    """
    with open(srt_filename, 'w') as f:
        start_time = 0

        for i, (text_chunk, chunk_duration) in enumerate(zip(text_chunks, chunk_durations)):
            end_time = start_time + chunk_duration

            # Viết ra định dạng SRT
            f.write(f"{i+1}\n")
            f.write(f"{format_srt_time(start_time)} --> {format_srt_time(end_time)}\n")
            f.write(f"{text_chunk}\n\n")

            start_time = end_time

def format_srt_time(seconds):
    """
    Chuyển đổi thời gian tính bằng giây thành định dạng SRT (hh:mm:ss,ms).
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 1000)
    return f"{hours:02}:{minutes:02}:{secs:02},{millis:03}"

# Load video và âm thanh
video = VideoFileClip("input_video.mp4")
audio = AudioFileClip("audio.mp3")

# Lấy thời lượng của file âm thanh
video_duration = audio.duration

# Nội dung văn bản
story_text = """
In a quiet village where the sky brushes the fields in hues of gold, young Mia discovered a map leading to forgotten treasures. Little did she know, her cat Whiskers had a secret: he was the guardian of the map, tasked with guiding Mia to not only the treasure but also to her destiny.
"""

# Chia câu chuyện thành các đoạn text
text_chunks = split_text(story_text)

# Tính toán thời lượng cho từng đoạn text
chunk_durations = calculate_duration_per_chunk(text_chunks, video_duration)

# Tạo file SRT
srt_filename = "output_subtitles.srt"
create_srt_file(text_chunks, chunk_durations, srt_filename)

# Cắt video sao cho khớp với độ dài của file âm thanh
video = video.subclip(0, video_duration)

# Thêm âm thanh vào video
final_video = video.set_audio(audio)

# Xuất video không có phụ đề
final_video.write_videofile("output_video_no_sub.mp4", fps=30)


# Sử dụng ffmpeg để thêm phụ đề SRT vào video
output_video_with_subtitles = "done.mp4"
os.system(f"ffmpeg -i output_video_no_sub.mp4 -vf subtitles={srt_filename} -c:a copy {output_video_with_subtitles}")
