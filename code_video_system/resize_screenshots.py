#!/usr/bin/env python3
"""
Resize all screenshots to 1920x1080 with proper scaling and centering
"""

from PIL import Image
import os

# Target resolution
TARGET_WIDTH = 1920
TARGET_HEIGHT = 1080

# Background color (dark gray to match code theme)
BACKGROUND_COLOR = '#2d2d2d'

# Create output directory
output_dir = "pic_resized"
os.makedirs(output_dir, exist_ok=True)

print(f"Resizing screenshots to {TARGET_WIDTH}x{TARGET_HEIGHT}...")

# Process all PNG files in pic directory
pic_files = [f for f in os.listdir('pic') if f.endswith('.png')]

for filename in pic_files:
    input_path = os.path.join('pic', filename)
    output_path = os.path.join(output_dir, filename)
    
    print(f"\nProcessing {filename}...")
    
    # Open the original image
    img = Image.open(input_path)
    original_width, original_height = img.size
    print(f"  Original size: {original_width}x{original_height}")
    
    # Calculate scaling factor to fit within target resolution while maintaining aspect ratio
    scale_x = TARGET_WIDTH / original_width
    scale_y = TARGET_HEIGHT / original_height
    scale = min(scale_x, scale_y) * 0.9  # Use 90% to leave some padding
    
    # Calculate new dimensions
    new_width = int(original_width * scale)
    new_height = int(original_height * scale)
    
    # Resize the image with high quality
    resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    # Create a new image with target resolution and background color
    final_img = Image.new('RGB', (TARGET_WIDTH, TARGET_HEIGHT), BACKGROUND_COLOR)
    
    # Calculate position to center the resized image
    x_offset = (TARGET_WIDTH - new_width) // 2
    y_offset = (TARGET_HEIGHT - new_height) // 2
    
    # Paste the resized image onto the background
    final_img.paste(resized_img, (x_offset, y_offset))
    
    # Save the final image
    final_img.save(output_path, quality=95, dpi=(300, 300))
    print(f"  ✓ Saved to {output_path}")
    print(f"  Resized to: {new_width}x{new_height} (scale: {scale:.2f})")
    print(f"  Centered at: ({x_offset}, {y_offset})")

print(f"\n✓ All screenshots resized and saved to '{output_dir}' directory")

# Update create_video.py to use resized images
print("\nUpdating video creation script to use resized images...")

# Read the current create_video.py
with open('create_video.py', 'r') as f:
    content = f.read()

# Replace pic/ with pic_resized/
updated_content = content.replace('pic/', 'pic_resized/')

# Write the updated content
with open('create_video_resized.py', 'w') as f:
    f.write(updated_content)

print("✓ Created 'create_video_resized.py' that uses resized images")