"""
Helper script to execute chatbot.py, workflow.py, and agent.py,
capture their live stdout outputs, and render authentic terminal screenshots
into Output/ (chatbot_output.png, workflow_output.png, agent_output.png).
"""
import os
import sys
import subprocess
from PIL import Image, ImageDraw, ImageFont


def render_terminal_screenshot(text_content: str, output_image_path: str, title: str):
    """Renders stdout text into a dark-themed terminal window PNG image."""
    lines = text_content.splitlines()
    if not lines:
        lines = ["(No output)"]

    # Terminal styling parameters
    font_size = 14
    padding = 20
    header_height = 36
    line_height = 20
    
    # Try to load a monospaced font, fallback to default font if unavailable
    try:
        font = ImageFont.truetype("consola.ttf", font_size)
    except Exception:
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except Exception:
            font = ImageFont.load_default()

    # Calculate required image dimensions
    max_line_len = max(len(line) for line in lines) if lines else 40
    img_width = max(800, max_line_len * 9 + padding * 2)
    img_height = header_height + padding * 2 + len(lines) * line_height

    # Colors (Dark Theme)
    bg_color = (30, 30, 30)          # #1E1E1E background
    header_color = (45, 45, 45)      # #2D2D2D title bar
    text_color = (220, 220, 220)     # light gray text
    title_color = (180, 180, 180)    # title text
    
    image = Image.new("RGB", (img_width, img_height), bg_color)
    draw = ImageDraw.Draw(image)

    # Draw header bar
    draw.rectangle([(0, 0), (img_width, header_height)], fill=header_color)
    
    # Window action buttons (red, yellow, green circles)
    button_y = header_height // 2
    draw.ellipse([(14, button_y - 6), (26, button_y + 6)], fill=(255, 95, 86))
    draw.ellipse([(34, button_y - 6), (46, button_y + 6)], fill=(255, 189, 46))
    draw.ellipse([(54, button_y - 6), (66, button_y + 6)], fill=(39, 201, 63))

    # Window title
    draw.text((80, (header_height - font_size) // 2), title, fill=title_color, font=font)

    # Draw stdout lines
    y = header_height + padding
    for line in lines:
        draw.text((padding, y), line, fill=text_color, font=font)
        y += line_height

    image.save(output_image_path)
    print(f"Generated screenshot: {output_image_path}")


def main():
    output_dir = os.path.join(os.path.dirname(__file__), "Output")
    os.makedirs(output_dir, exist_ok=True)

    python_executable = sys.executable

    tasks = [
        ("chatbot.py", "chatbot_output.png", "chatbot_output.txt", "System 1 — Plain Chatbot Terminal Output"),
        ("workflow.py", "workflow_output.png", "workflow_output.txt", "System 2 — Rule-Based Workflow Terminal Output"),
        ("agent.py", "agent_output.png", "agent_output.txt", "System 3 — AI Agent Terminal Output"),
    ]

    for script_file, img_filename, txt_filename, title in tasks:
        print(f"\nRunning {script_file}...")
        result = subprocess.run(
            [python_executable, script_file],
            capture_output=True,
            text=True,
            encoding="utf-8",
            cwd=os.path.dirname(__file__)
        )
        stdout_text = result.stdout
        if result.stderr:
            stdout_text += f"\nSTDERR:\n{result.stderr}"

        # Save text log
        txt_path = os.path.join(output_dir, txt_filename)
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(stdout_text)

        # Generate PNG image screenshot
        img_path = os.path.join(output_dir, img_filename)
        render_terminal_screenshot(stdout_text, img_path, title)


if __name__ == "__main__":
    main()
