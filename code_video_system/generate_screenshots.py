#!/usr/bin/env python3
"""
Generate screenshot images for each scene of rbeta.py
"""

import os
import sys
from code_to_image_simple import SimpleCodeImageGenerator

# Read the source code
with open('rbeta.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Define scenes with their line ranges and output filenames
scenes = [
    {'name': 'scene01_import', 'start': 1, 'end': 3},
    {'name': 'scene02_settings', 'start': 5, 'end': 10},
    {'name': 'scene03_calculate_resize', 'start': 13, 'end': 41},
    {'name': 'scene04_resize_image', 'start': 44, 'end': 56},
    {'name': 'scene05_validation', 'start': 59, 'end': 75},
    {'name': 'scene06_output_folder', 'start': 77, 'end': 83},
    {'name': 'scene07_main_loop_start', 'start': 85, 'end': 100},
    {'name': 'scene08_image_processing', 'start': 102, 'end': 134},
    {'name': 'scene09_error_handling', 'start': 136, 'end': 141},
    {'name': 'scene10_summary', 'start': 143, 'end': 148}
]

# Create image generator (using light theme for better visibility)
generator = SimpleCodeImageGenerator(theme='light', font_size=16)

# Generate screenshots for each scene
for scene in scenes:
    # Extract the relevant lines (adjusting for 0-based indexing)
    scene_lines = lines[scene['start']-1:scene['end']]
    scene_code = ''.join(scene_lines)
    
    # Generate the image
    output_path = f"pic/{scene['name']}.png"
    title = f"rbeta.py - Lines {scene['start']}-{scene['end']}"
    
    print(f"Generating {output_path}...")
    generator.generate_image(scene_code, output_path, title=title)

print("\nAll screenshots generated successfully!")