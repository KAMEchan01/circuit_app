#!/usr/bin/env python3
"""
Simple Code to Image Converter
Converts Python source code to a screenshot-like image without external syntax highlighting libraries.
Only requires Pillow (PIL).

Requirements:
    pip install pillow
"""

import sys

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("Error: Pillow library is not installed.")
    print("Please install it using: pip install pillow")
    sys.exit(1)

import os
import re


class SimpleCodeImageGenerator:
    """Generates screenshot-like images from source code with basic syntax highlighting."""
    
    # Theme configurations
    THEMES = {
        'dark': {
            'background': '#1e1e1e',
            'line_number_bg': '#2d2d2d',
            'line_number_fg': '#858585',
            'default_text': '#d4d4d4',
            'keyword': '#569cd6',
            'string': '#ce9178',
            'comment': '#6a9955',
            'function': '#dcdcaa',
            'number': '#b5cea8',
            'decorator': '#d7ba7d'
        },
        'light': {
            'background': '#ffffff',
            'line_number_bg': '#f5f5f5',
            'line_number_fg': '#999999',
            'default_text': '#333333',
            'keyword': '#0000ff',
            'string': '#a31515',
            'comment': '#008000',
            'function': '#795e26',
            'number': '#098658',
            'decorator': '#af00db'
        }
    }
    
    # Python keywords
    KEYWORDS = {
        'False', 'None', 'True', 'and', 'as', 'assert', 'async', 'await',
        'break', 'class', 'continue', 'def', 'del', 'elif', 'else', 'except',
        'finally', 'for', 'from', 'global', 'if', 'import', 'in', 'is',
        'lambda', 'nonlocal', 'not', 'or', 'pass', 'raise', 'return', 'try',
        'while', 'with', 'yield', 'self'
    }
    
    # Built-in functions
    BUILTINS = {
        'abs', 'all', 'any', 'ascii', 'bin', 'bool', 'bytearray', 'bytes',
        'callable', 'chr', 'classmethod', 'compile', 'complex', 'delattr',
        'dict', 'dir', 'divmod', 'enumerate', 'eval', 'exec', 'filter',
        'float', 'format', 'frozenset', 'getattr', 'globals', 'hasattr',
        'hash', 'help', 'hex', 'id', 'input', 'int', 'isinstance', 'issubclass',
        'iter', 'len', 'list', 'locals', 'map', 'max', 'memoryview', 'min',
        'next', 'object', 'oct', 'open', 'ord', 'pow', 'print', 'property',
        'range', 'repr', 'reversed', 'round', 'set', 'setattr', 'slice',
        'sorted', 'staticmethod', 'str', 'sum', 'super', 'tuple', 'type',
        'vars', 'zip'
    }
    
    def __init__(self, theme='dark', font_size=14, line_height_ratio=1.5):
        """Initialize the code image generator."""
        self.theme = self.THEMES.get(theme, self.THEMES['dark'])
        self.font_size = font_size
        self.line_height = int(font_size * line_height_ratio)
        
        # Try to load a monospace font
        self.font = self._load_font()
        
        # Margins and padding
        self.padding = 30
        self.line_number_padding = 15
        self.line_number_width = 50
        
    def _load_font(self):
        """Load a suitable monospace font."""
        return self._load_font_with_size(self.font_size)
    
    def _load_font_with_size(self, size):
        """Load a suitable monospace font with specific size."""
        font_candidates = [
            # macOS - Japanese fonts first
            '/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc',
            '/System/Library/Fonts/Hiragino Sans GB.ttc',
            '/Library/Fonts/Arial Unicode.ttf',
            '/System/Library/Fonts/PingFang.ttc',
            # macOS - English monospace fonts
            '/System/Library/Fonts/Monaco.dfont',
            '/Library/Fonts/Courier New.ttf',
            '/System/Library/Fonts/Menlo.ttc',
            # Linux - Japanese fonts
            '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
            '/usr/share/fonts/truetype/fonts-japanese-gothic.ttf',
            # Linux - English fonts
            '/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf',
            '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf',
            # Windows - Japanese fonts
            'C:\\Windows\\Fonts\\msgothic.ttc',
            'C:\\Windows\\Fonts\\YuGothM.ttc',
            # Windows - English fonts
            'C:\\Windows\\Fonts\\consola.ttf',
            'C:\\Windows\\Fonts\\cour.ttf',
        ]
        
        for font_path in font_candidates:
            if os.path.exists(font_path):
                try:
                    return ImageFont.truetype(font_path, size)
                except:
                    continue
        
        # Fallback to default font
        try:
            return ImageFont.load_default()
        except:
            print("Warning: Could not load font, using PIL default")
            return ImageFont.load_default()
    
    def _get_text_size(self, text):
        """Get the size of text when rendered."""
        bbox = self.font.getbbox(text)
        return bbox[2] - bbox[0], bbox[3] - bbox[1]
    
    def _tokenize_line(self, line):
        """Simple tokenizer for Python code."""
        tokens = []
        
        # Handle empty lines
        if not line.strip():
            return [(line, 'default')]
        
        # Check if entire line is a comment
        if line.strip().startswith('#'):
            return [(line, 'comment')]
        
        # Regular expressions for different token types
        patterns = [
            (r'#.*$', 'comment'),  # Comments
            (r'@\w+', 'decorator'),  # Decorators
            (r'""".*?"""|\'\'\'.*?\'\'\'', 'string'),  # Triple quotes
            (r'"[^"]*"|\'[^\']*\'', 'string'),  # Strings
            (r'\b\d+\.?\d*\b', 'number'),  # Numbers
            (r'\b(?:' + '|'.join(self.KEYWORDS) + r')\b', 'keyword'),  # Keywords
            (r'\b(?:' + '|'.join(self.BUILTINS) + r')\b', 'function'),  # Built-ins
            (r'\b\w+(?=\s*\()', 'function'),  # Function calls
        ]
        
        # Tokenize the line
        position = 0
        while position < len(line):
            matched = False
            
            for pattern, token_type in patterns:
                regex = re.compile(pattern)
                match = regex.match(line, position)
                if match:
                    # Add any text before the match as default
                    if match.start() > position:
                        tokens.append((line[position:match.start()], 'default'))
                    
                    # Add the matched token
                    tokens.append((match.group(), token_type))
                    position = match.end()
                    matched = True
                    break
            
            if not matched:
                # No pattern matched, add one character as default
                tokens.append((line[position], 'default'))
                position += 1
        
        return tokens
    
    def generate_image(self, code, output_path, title=None):
        """Generate an image from source code."""
        # Split code into lines
        lines = code.split('\n')
        num_lines = len(lines)
        
        # Calculate image dimensions
        max_line_length = max(len(line) for line in lines) if lines else 0
        char_width, _ = self._get_text_size('M')
        
        content_width = (max_line_length * char_width) + self.line_number_width + (self.line_number_padding * 2)
        content_height = num_lines * self.line_height
        
        img_width = content_width + (self.padding * 2)
        img_height = content_height + (self.padding * 2)
        
        if title:
            img_height += self.line_height + 10
        
        # Create image with higher resolution for better quality
        scale = 4  # Scale factor for higher resolution (increased from 2 to 4)
        img = Image.new('RGB', (img_width * scale, img_height * scale), self.theme['background'])
        draw = ImageDraw.Draw(img)
        
        # Create scaled font
        scaled_font = self._load_font_with_size(self.font_size * scale)
        
        # Draw title if provided
        y_offset = self.padding * scale
        if title:
            title_color = self.theme['default_text']
            draw.text((self.padding * scale, y_offset), title, fill=title_color, font=scaled_font)
            y_offset += (self.line_height + 10) * scale
        
        # Draw line numbers background
        line_num_bg_x1 = self.padding * scale
        line_num_bg_x2 = (self.padding + self.line_number_width) * scale
        draw.rectangle(
            [line_num_bg_x1, y_offset, line_num_bg_x2, y_offset + (content_height * scale)],
            fill=self.theme['line_number_bg']
        )
        
        # Process each line
        for i, line in enumerate(lines):
            line_y = y_offset + (i * self.line_height * scale)
            
            # Draw line number
            line_num = str(i + 1).rjust(3)
            draw.text(
                ((self.padding + 5) * scale, line_y),
                line_num,
                fill=self.theme['line_number_fg'],
                font=scaled_font
            )
            
            # Draw code line with syntax highlighting
            x_offset = (self.padding + self.line_number_width + self.line_number_padding) * scale
            
            # Tokenize and draw the line
            tokens = self._tokenize_line(line)
            for token_text, token_type in tokens:
                color = self.theme.get(token_type, self.theme['default_text'])
                draw.text(
                    (x_offset, line_y),
                    token_text,
                    fill=color,
                    font=scaled_font
                )
                text_width = scaled_font.getbbox(token_text)[2]
                x_offset += text_width
        
        # Add a subtle border
        border_color = '#333333' if 'dark' in self.theme else '#cccccc'
        draw.rectangle(
            [0, 0, (img_width * scale) - 1, (img_height * scale) - 1],
            outline=border_color,
            width=scale
        )
        
        # Add subtle shadow/gradient effect at edges
        for i in range(10):
            alpha = 255 - (i * 20)
            shadow_color = (0, 0, 0, alpha) if 'dark' in self.theme else (200, 200, 200, alpha)
            # Top shadow
            draw.line([(i, i), ((img_width * scale) - i, i)], fill=shadow_color, width=1)
            # Left shadow
            draw.line([(i, i), (i, (img_height * scale) - i)], fill=shadow_color, width=1)
        
        # Resize back to target resolution with antialiasing
        img = img.resize((img_width, img_height), Image.Resampling.LANCZOS)
        
        # Save image with higher quality
        img.save(output_path, quality=100, dpi=(600, 600))
        print(f"Image saved to: {output_path}")


def main():
    """Main function to convert Python files to images."""
    
    # Parse command line arguments
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    else:
        input_file = 'rbeta.py'
    
    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found.")
        print("\nUsage:")
        print("  python code_to_image_simple.py [filename]")
        print("\nExample:")
        print("  python code_to_image_simple.py rbeta.py")
        print("  python code_to_image_simple.py mycode.py")
        print("\nNote: This script only requires the Pillow library.")
        print("Install it with: pip install pillow")
        sys.exit(1)
    
    # Read source code
    with open(input_file, 'r', encoding='utf-8') as f:
        code = f.read()
    
    # Get base filename without extension
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    
    # Generate images with both themes
    generator_dark = SimpleCodeImageGenerator(theme='dark', font_size=14)
    generator_light = SimpleCodeImageGenerator(theme='light', font_size=14)
    
    # Generate dark theme image
    output_dark = f'{base_name}_dark_simple.png'
    generator_dark.generate_image(
        code,
        output_dark,
        title=f'{os.path.basename(input_file)} - Dark Theme'
    )
    
    # Generate light theme image
    output_light = f'{base_name}_light_simple.png'
    generator_light.generate_image(
        code,
        output_light,
        title=f'{os.path.basename(input_file)} - Light Theme'
    )
    
    print(f"\nSuccessfully generated:")
    print(f"  - Dark theme: {output_dark}")
    print(f"  - Light theme: {output_light}")


if __name__ == '__main__':
    main()