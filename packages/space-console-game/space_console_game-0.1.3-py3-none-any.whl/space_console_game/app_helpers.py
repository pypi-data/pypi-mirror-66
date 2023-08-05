import asyncio
import os


async def sleep(delay: int = 1) -> None:
    """Async sleep function."""
    for _ in range(delay):
        await asyncio.sleep(0)


def get_rocket_frame_content(filepath: str) -> str:
    """Get rocket frame."""
    with open(os.path.abspath(filepath), 'r') as file_object:
        return file_object.read()
