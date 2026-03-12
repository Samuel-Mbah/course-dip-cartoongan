import os
import subprocess

def extract_frames(video_path, output_dir, interval=1):
    """
    Extract frames from a video at a given interval.
    Args:
        video_path (str): Path to the video file.
        output_dir (str): Directory to save the extracted frames.
        interval (int): Interval in seconds to extract frames.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    ffmpeg_path = os.environ.get('FFMPEG_PATH', 'ffmpeg')  # Set FFMPEG_PATH env var if ffmpeg is not on PATH

    command = [
        ffmpeg_path,
        '-i', video_path,
        '-vf', f'fps=1/{interval}',
        os.path.join(output_dir, 'frame_%04d.png')
    ]

    subprocess.run(command, check=True)
    print(f'Extracted frames from {video_path} to {output_dir}')

# Example usage:
videos = {
    'Makoto Shinkai': ['AnimePahe_Suzume_no_Tojimari_-_01_BD_804p_Lazy.mp4', 'AnimePahe_Kimi_no_Na_wa._-_01_BD_1080p_MTBB.mp4'],
    'Mamoru Hosoda': ['AnimePahe_Ookami_Kodomo_no_Ame_to_Yuki_-_01_BD_1076p_Commie.mp4', 'AnimePahe_Mirai_no_Mirai_-_01_BD_1036p_WiKi.mp4'],
    'Miyazaki Hayao': ['Spirited.Away_.2001-WWW.STARAZI.COM_ (1).mp4'],
    'Paprika': ['AnimePahe_Paprika_-_01_BD_992p_Afro.mp4']
}

for artist, video_paths in videos.items():
    for video_path in video_paths:
        output_dir = f'Cartoon_data/cartoon_images/{artist}'
        extract_frames(video_path, output_dir, interval=1)
