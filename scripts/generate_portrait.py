from PIL import Image, ImageOps, ImageEnhance

INPUT_IMAGE = "assets/portrait.jpg"
OUTPUT_IMAGE = "assets/portrait.svg"

# ASCII characters from dark to bright
ASCII_CHARS = "@%#*+=-:. "


def image_to_ascii(image, width=90):
    # Keep the original aspect ratio.
    # Characters are taller than they are wide,
    # so we compensate for that here.
    aspect_ratio = image.height / image.width
    height = int(width * aspect_ratio * 0.5)

    image = image.resize((width, height))

    # Convert to grayscale
    image = ImageOps.grayscale(image)

    # Improve contrast
    image = ImageEnhance.Contrast(image).enhance(1.5)

    pixels = list(image.getdata())

    ascii_image = []

    for y in range(height):
        row = ""

        for x in range(width):
            brightness = pixels[y * width + x]

            index = int(
                brightness / 255 * (len(ASCII_CHARS) - 1)
            )

            row += ASCII_CHARS[index]

        ascii_image.append(row)

    return ascii_image


def create_svg(ascii_art):
    width = len(ascii_art[0])
    height = len(ascii_art)

    char_width = 8
    char_height = 12

    svg_width = width * char_width
    svg_height = height * char_height

    text_lines = []

    for row_number, row in enumerate(ascii_art):
        escaped_row = (
            row.replace("&", "&amp;")
               .replace("<", "&lt;")
               .replace(">", "&gt;")
        )

        y = (row_number + 1) * char_height

        text_lines.append(
            f'<text x="0" y="{y}">{escaped_row}</text>'
        )

    text_content = "\n".join(text_lines)

    svg = f"""<?xml version="1.0" encoding="UTF-8"?>

<svg
    xmlns="http://www.w3.org/2000/svg"
    width="{svg_width}"
    height="{svg_height}"
    viewBox="0 0 {svg_width} {svg_height}">

    <rect
        width="100%"
        height="100%"
        fill="#0d1117"/>

    <g
        fill="#ffffff"
        font-family="monospace"
        font-size="{char_height}px"
        xml:space="preserve">

        {text_content}

    </g>

</svg>
"""

    return svg


def main():
    print("Loading image...")

    image = Image.open(INPUT_IMAGE)

    print("Creating ASCII portrait...")

    ascii_art = image_to_ascii(image)

    print("Creating SVG...")

    svg = create_svg(ascii_art)

    with open(OUTPUT_IMAGE, "w", encoding="utf-8") as file:
        file.write(svg)

    print("Portrait created!")
    print(f"Saved to: {OUTPUT_IMAGE}")


if __name__ == "__main__":
    main()
