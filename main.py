import random
import sys
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, AudioFileClip

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

def count_words(text):
    # Split the text by spaces and count the words
    words = text.split()
    return len(words)

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

# Load video và âm thanh
video = VideoFileClip("input_video.mp4")
audio = AudioFileClip("audio1.mp3")

# Lấy thời lượng của file âm thanh
video_duration = audio.duration

# Nội dung văn bản
story_text = """
In a quiet village where the sky brushes the fields in hues of gold, young Mia discovered a map leading to forgotten treasures. Little did she know, her cat Whiskers had a secret: he was the guardian of the map, tasked with guiding Mia to not only the treasure but also to her destiny.
"""

# Chia câu chuyện thành các đoạn text
text_chunks = split_text(story_text)

word_count = count_words(story_text)

second_per_word = video_duration/word_count

words_per_second = 1 / second_per_word


# print(words_per_second, word_count)
# sys.exit();

# Tính toán thời lượng cho từng đoạn text
chunk_durations = calculate_duration_per_chunk(text_chunks, video_duration, words_per_second)

# Cắt video sao cho khớp với độ dài của file âm thanh
video = video.subclip(0, video_duration)

# Tạo danh sách các đoạn video chứa text
video_clips = []
start_time = 0
font_path = "font1.otf"

# Tạo đoạn text và thêm vào video cho từng chunk
for i, (text_chunk, chunk_duration) in enumerate(zip(text_chunks, chunk_durations)):
    # Tạo đoạn text cho mỗi chunk
    text_clip = TextClip(text_chunk, font=font_path, fontsize=40, color='white', stroke_color='black', stroke_width=2, size=(video.w, video.h//10))  
    text_clip = text_clip.set_position(('center', 'center')).set_start(start_time).set_duration(chunk_duration)

    # Cập nhật thời gian bắt đầu cho đoạn tiếp theo
    start_time += chunk_duration

    # Chèn đoạn text vào video
    video_clips.append(text_clip)

# Ghép các text clip với video gốc
final_video = CompositeVideoClip([video] + video_clips)

# Thêm âm thanh vào video
final_video = final_video.set_audio(audio)

# Xuất video cuối cùng
final_video.write_videofile("ok1.mp4", fps=30)
