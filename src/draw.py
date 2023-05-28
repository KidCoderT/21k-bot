from contextlib import contextmanager
from pathlib import Path
from PIL import Image, ImageFont, ImageDraw

TEMP_DIR = Path.cwd().parent / "temp/"
TEMP_DIR.mkdir(exist_ok=True)


def draw_progress_bar(d, x, y, w, h, progress, bg="#D9D9D9", fg="#233973"):
    # draw background
    d.ellipse((x + w, y, x + h + w, y + h), fill=bg)
    d.ellipse((x, y, x + h, y + h), fill=bg)
    d.rectangle((x + (h / 2), y, x + w + (h / 2), y + h), fill=bg)

    # draw progress bar
    w *= progress
    d.ellipse((x + w, y, x + h + w, y + h), fill=fg)
    d.ellipse((x, y, x + h, y + h), fill=fg)
    d.rectangle((x + (h / 2), y, x + w + (h / 2), y + h), fill=fg)

    font = ImageFont.truetype("arial.ttf", 12 * 16)
    d.text(
        (x + w - (12 * 8) * 2.5, y + 8),
        f"{int(progress * 100)}%",
        fill="white",
        font=font,
    )

    return d


@contextmanager
def stats_img(
    assignments_done: tuple[int, int],
    assignments_avg_score: float,
    attendance: tuple[int, int],
):
    bar_x = 16 * 10
    bar_width = 250 * 10
    bar_height = 24 * 10
    bar_spacing = 18 * 10
    bar_offset = 28 * 10

    img_height = bar_offset * 2 + bar_height * 3 + bar_spacing * 2

    # Create a canvas 357 pixels in length and 99 pixels in height
    canvas = Image.new("RGB", (int(img_height * 3.5), img_height), "white")
    draw = ImageDraw.Draw(canvas)

    # Set the font for text
    font = ImageFont.truetype("arial.ttf", 12 * 18)

    # Define the positions and dimensions for the progress bars

    # Draw the progress bars and labels
    labels = ["Assignments Done %", "Assignments Avg Score %", "Attendance %"]
    progress_values = [
        assignments_done[0] / assignments_done[1],
        assignments_avg_score,
        attendance[0] / attendance[1],
    ]

    for i, label in enumerate(labels):
        y = bar_offset + i * (bar_height + bar_spacing)
        draw.text(
            (bar_x + bar_width + bar_height + 80, y), label, fill="black", font=font
        )
        draw_progress_bar(draw, bar_x, y, bar_width, bar_height, progress_values[i])

    # Save the image to a file
    image_path = TEMP_DIR / f"{hash(font)}-stats_image.png"
    canvas.reduce(6).save(image_path)

    yield image_path

    image_path.unlink()


if __name__ == "__main__":
    with stats_img((23, 44), 0.34, (500, 600)) as f:
        input()
