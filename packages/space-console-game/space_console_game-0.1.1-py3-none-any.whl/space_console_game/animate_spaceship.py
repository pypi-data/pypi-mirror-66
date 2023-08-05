from typing import List

from space_console_game.app_helpers import sleep
from space_console_game.curses_tools import (
    draw_frame,
    get_frame_size,
    read_controls,
)


async def animate_spaceship(
    canvas,
    rocket_frames: List[str],
    canvas_height: int,
    canvas_width: int,
) -> None:
    """Display animation of spaceship."""
    row, column = canvas_height / 2, canvas_width / 2

    spaceship_height, spaceship_width = get_frame_size(rocket_frames[0])

    while True:
        rows_direction, columns_direction, space_pressed = read_controls(canvas)

        if 0 < row + rows_direction < canvas_height - spaceship_height:
            row += rows_direction
        if 0 < column + columns_direction < canvas_width - spaceship_width:
            column += columns_direction

        for rocket_frame in rocket_frames:
            draw_frame(canvas, int(row), int(column), rocket_frame)
            await sleep(3)
            draw_frame(canvas, int(row), int(column), rocket_frame, negative=True)
