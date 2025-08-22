#!/usr/bin/env python3
"""
Create video from screenshots and audio narration using ffmpeg
"""

import subprocess
import os

# Video settings
output_video = "rbeta_tutorial.mp4"
resolution = "1920x1080"
fps = 30
video_codec = "libx264"
audio_codec = "aac"

# Define scenes with their durations (including 1 second gap after each scene)
scenes = [
    {'id': 'scene01', 'duration': 7.4, 'gap': 1.0},
    {'id': 'scene02', 'duration': 17.7, 'gap': 1.0},
    {'id': 'scene03', 'duration': 16.5, 'gap': 1.0},
    {'id': 'scene04', 'duration': 9.9, 'gap': 1.0},
    {'id': 'scene05', 'duration': 16.6, 'gap': 1.0},
    {'id': 'scene06', 'duration': 6.6, 'gap': 1.0},
    {'id': 'scene07', 'duration': 9.6, 'gap': 1.0},
    {'id': 'scene08', 'duration': 19.8, 'gap': 1.0},
    {'id': 'scene09', 'duration': 10.7, 'gap': 1.0},
    {'id': 'scene10', 'duration': 8.7, 'gap': 0.0},  # No gap after last scene
]

# Create a temporary directory for intermediate files
temp_dir = "temp_video_files"
os.makedirs(temp_dir, exist_ok=True)

print("Creating video segments for each scene...")

# Process each scene
for i, scene in enumerate(scenes):
    scene_id = scene['id']
    duration = scene['duration']
    gap = scene['gap']
    total_duration = duration + gap
    
    print(f"\nProcessing {scene_id}...")
    
    # Create video from image
    image_file = f"pic_resized/{scene_id}_import.png" if scene_id == 'scene01' else f"pic_resized/{scene_id}_{scene_id.replace('scene', '').replace('0', '')}.png"
    
    # Check for correct image filename
    possible_image_files = [
        f"pic_resized/{scene_id}_import.png",
        f"pic_resized/{scene_id}_settings.png",
        f"pic_resized/{scene_id}_calculate_resize.png",
        f"pic_resized/{scene_id}_resize_image.png",
        f"pic_resized/{scene_id}_validation.png",
        f"pic_resized/{scene_id}_output_folder.png",
        f"pic_resized/{scene_id}_main_loop_start.png",
        f"pic_resized/{scene_id}_image_processing.png",
        f"pic_resized/{scene_id}_error_handling.png",
        f"pic_resized/{scene_id}_summary.png"
    ]
    
    image_file = None
    for possible_file in possible_image_files:
        if os.path.exists(possible_file):
            image_file = possible_file
            break
    
    if not image_file:
        print(f"  ✗ Error: Image file for {scene_id} not found")
        continue
    
    audio_file = f"audio/{scene_id}_narration.mp3"
    video_segment = f"{temp_dir}/{scene_id}_video.mp4"
    
    # Create video segment with audio
    cmd = [
        'ffmpeg',
        '-loop', '1',
        '-i', image_file,
        '-i', audio_file,
        '-c:v', video_codec,
        '-tune', 'stillimage',
        '-c:a', audio_codec,
        '-b:a', '192k',
        '-pix_fmt', 'yuv420p',
        '-s', resolution,
        '-r', str(fps),
        '-t', str(total_duration),
        '-shortest',
        video_segment,
        '-y'
    ]
    
    try:
        subprocess.run(cmd, check=True, capture_output=True)
        print(f"  ✓ Created video segment: {video_segment}")
    except subprocess.CalledProcessError as e:
        print(f"  ✗ Error creating video segment: {e}")
        print(f"    stderr: {e.stderr.decode()}")
        continue

# Create concat file
concat_file = f"{temp_dir}/concat.txt"
with open(concat_file, 'w') as f:
    for scene in scenes:
        video_file = f"{temp_dir}/{scene['id']}_video.mp4"
        if os.path.exists(video_file):
            f.write(f"file '{os.path.abspath(video_file)}'\n")

print("\nConcatenating all video segments...")

# Concatenate all videos
concat_cmd = [
    'ffmpeg',
    '-f', 'concat',
    '-safe', '0',
    '-i', concat_file,
    '-c', 'copy',
    output_video,
    '-y'
]

try:
    subprocess.run(concat_cmd, check=True, capture_output=True)
    print(f"\n✓ Successfully created video: {output_video}")
    
    # Get video info
    probe_cmd = [
        'ffprobe',
        '-v', 'error',
        '-select_streams', 'v:0',
        '-show_entries', 'stream=width,height,r_frame_rate,duration',
        '-of', 'default=noprint_wrappers=1',
        output_video
    ]
    
    try:
        result = subprocess.run(probe_cmd, capture_output=True, text=True, check=True)
        print(f"\nVideo info:")
        print(result.stdout)
    except:
        pass
    
    # Get file size
    file_size = os.path.getsize(output_video) / (1024 * 1024)  # MB
    print(f"File size: {file_size:.2f} MB")
    
except subprocess.CalledProcessError as e:
    print(f"\n✗ Error concatenating videos: {e}")
    print(f"  stderr: {e.stderr.decode()}")

# Clean up temporary files
print("\nCleaning up temporary files...")
for file in os.listdir(temp_dir):
    os.remove(os.path.join(temp_dir, file))
os.rmdir(temp_dir)
print("✓ Cleanup complete")

print(f"\nVideo creation complete! Output file: {output_video}")