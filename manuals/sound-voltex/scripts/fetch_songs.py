import asyncio
import os
from pathlib import Path
import aiohttp
from bs4 import BeautifulSoup, Tag

from .lib.songs import Song


async def fetch_all_songs(page_count: int):
    print(f"fetching all songs from {page_count} pages...")

    songs: list[Song] = []

    async with aiohttp.ClientSession() as session:
        tasks = [
            fetch_page_songs(session, page_index + 1)
            for page_index in range(page_count)
        ]
        for result_index, page_songs in enumerate(await asyncio.gather(*tasks)):
            songs += page_songs
            # todo: print this on future finish
            print(f"fetched {len(songs)} songs ({result_index+1}/{page_count})")

    return songs


async def fetch_page_songs(session: aiohttp.ClientSession, page_number: int):
    url = f"https://www.myshkin.io/sdvx/songlist?page={page_number}"

    async with session.get(url) as response:
        html_content = await response.text()

    soup = BeautifulSoup(html_content, "html5lib")
    return [parse_song(row) for row in soup.select("#song-table-body > tr")]


def parse_song(row: Tag):
    title_element = row.select_one(".song-title")
    title = title_element.get_text(strip=True) if title_element else "Unknown Title"

    artist_element = row.select_one(".song-artist")
    artist = artist_element.get_text(strip=True) if artist_element else "Unknown Artist"

    groups = ["Unknown Group"]
    genre_header = None
    for header in row.select(".metadata-header"):
        if "Genre" in header.get_text():
            genre_header = header
            break

    if genre_header and (next_sibling := genre_header.find_next_sibling()):
        groups = [part.strip() for part in next_sibling.get_text().split(",")]

    charts: dict[str, int] = {}
    for cell in row.select(".chart-difficulty"):
        cell_text = cell.get_text(strip=True)
        parts = cell_text.split(" ")
        if len(parts) >= 2:
            key = parts[0]
            level = parts[1]
            try:
                charts[key] = int(level)
            except ValueError:
                print(f"failed to parse difficulty cell: {cell_text}")
                continue
        else:
            print(f"failed to parse difficulty cell: {cell_text}")
            continue

    return Song(
        identifier=f"{title} by {artist}",
        title=title,
        artist=artist,
        groups=groups,
        charts=charts,
    )


if __name__ == "__main__":
    songs = asyncio.run(fetch_all_songs(53))
    songs.sort(key=lambda song: song.title)

    print(f"saving {len(songs)} songs...")

    data_dir = Path(__file__).parent.parent / "src/data"
    songs_file_path = data_dir / "songs.json"

    os.makedirs(data_dir, exist_ok=True)
    with open(songs_file_path, "w", encoding="utf-8") as file:
        file.write(
            Song.schema().dumps(songs, many=True, indent="\t", ensure_ascii=False)
        )

    print("done")
