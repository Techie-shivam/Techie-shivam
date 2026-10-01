import random

def generate_snake_svg(output_path, is_dark=True):
    bg_color = "#0d1117" if is_dark else "#ffffff"
    empty_color = "#161b22" if is_dark else "#ebedf0"
    
    green_shades = [
        "#0e4429" if is_dark else "#9be9a8",
        "#006d32" if is_dark else "#40c463",
        "#26a641" if is_dark else "#30a14e",
        "#39d353" if is_dark else "#216e39",
    ]

    cols = 53
    rows = 7
    square_size = 11
    gap = 3

    width = cols * (square_size + gap) + 30
    height = rows * (square_size + gap) + 30

    svg_content = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" fill="none">',
        '  <style>',
        f'    .bg {{ fill: {bg_color}; rx: 6px; }}',
        '    @keyframes snakeMove {',
        '      0% { transform: translate(0px, 0px); }',
        '      20% { transform: translate(160px, 42px); }',
        '      40% { transform: translate(320px, 0px); }',
        '      60% { transform: translate(480px, 56px); }',
        '      80% { transform: translate(640px, 14px); }',
        '      100% { transform: translate(720px, 42px); }',
        '    }',
        '    .snake { animation: snakeMove 10s infinite linear alternate; }',
        '  </style>',
        f'  <rect width="{width}" height="{height}" class="bg"/>',
        '  <g transform="translate(15, 15)">'
    ]

    random.seed(123)  # Balanced natural pattern (~700 contributions look)
    for col in range(cols):
        x = col * (square_size + gap)
        for row in range(rows):
            y = row * (square_size + gap)
            if random.random() < 0.65:
                color = random.choice(green_shades)
            else:
                color = empty_color
            svg_content.append(f'    <rect x="{x}" y="{y}" width="{square_size}" height="{square_size}" rx="2" fill="{color}"/>')

    svg_content.extend([
        '    <!-- Animated Snake -->',
        '    <g class="snake">',
        '      <rect x="0" y="0" width="11" height="11" rx="3" fill="#a855f7"/>',
        '      <rect x="-14" y="0" width="11" height="11" rx="2" fill="#c084fc"/>',
        '      <rect x="-28" y="0" width="11" height="11" rx="2" fill="#d8b4fe"/>',
        '      <rect x="-42" y="0" width="11" height="11" rx="2" fill="#e9d5ff"/>',
        '    </g>',
        '  </g>',
        '</svg>'
    ])

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg_content))

if __name__ == "__main__":
    generate_snake_svg("assets/github-snake-dark.svg", is_dark=True)
    generate_snake_svg("assets/github-snake.svg", is_dark=False)
    print("Created natural 700-contribution Snake SVGs in assets/")
