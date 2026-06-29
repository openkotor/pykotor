from __future__ import annotations

import io

from pathlib import Path

import pytest

from pykotor.cli.dispatch import cli_main
from pykotor.resource.formats.tpc.tga import read_tga

Image = pytest.importorskip("PIL.Image")


def _write_png(
    path: Path, color: tuple[int, int, int, int], size: tuple[int, int] = (2, 2)
) -> None:
    Image.new("RGBA", size, color).save(path)


def _write_png_pixels(
    path: Path,
    pixels: list[tuple[int, int, int, int]],
    size: tuple[int, int],
) -> None:
    image = Image.new("RGBA", size)
    image.putdata(pixels)
    image.save(path)


def test_texture_convert_batches_png_to_tga(tmp_path: Path) -> None:
    red = tmp_path / "red.png"
    green = tmp_path / "green.png"
    out_dir = tmp_path / "converted"
    red_pixels = [
        (255, 0, 0, 255),
        (0, 255, 0, 128),
        (0, 0, 255, 64),
        (255, 255, 0, 0),
    ]
    _write_png_pixels(red, red_pixels, (2, 2))
    _write_png(green, (0, 255, 0, 128))

    assert (
        cli_main(
            [
                "texture-convert",
                str(red),
                str(green),
                "--to",
                "tga",
                "--output",
                str(out_dir),
            ]
        )
        == 0
    )

    red_tga = read_tga(io.BytesIO((out_dir / "red.tga").read_bytes()))
    green_tga = read_tga(io.BytesIO((out_dir / "green.tga").read_bytes()))
    assert (red_tga.width, red_tga.height) == (2, 2)
    assert red_tga.data[:4] == bytes((255, 0, 0, 255))
    assert [tuple(red_tga.data[i : i + 4]) for i in range(0, len(red_tga.data), 4)] == red_pixels
    assert green_tga.data[:4] == bytes((0, 255, 0, 128))


def test_texture_convert_tga_to_png_roundtrip(tmp_path: Path) -> None:
    source_png = tmp_path / "source.png"
    source_tga = tmp_path / "source.tga"
    roundtrip_png = tmp_path / "roundtrip.png"
    _write_png(source_png, (12, 34, 56, 200))

    assert cli_main(["texture-convert", str(source_png), "--output", str(source_tga)]) == 0
    assert (
        cli_main(
            [
                "texture-convert",
                str(source_tga),
                "--to",
                "png",
                "--output",
                str(roundtrip_png),
            ]
        )
        == 0
    )

    with Image.open(roundtrip_png) as image:
        rgba = image.convert("RGBA")
        assert rgba.size == (2, 2)
        assert rgba.tobytes()[:4] == bytes((12, 34, 56, 200))


def test_texture_convert_recursive_output_preserves_relative_paths(tmp_path: Path) -> None:
    root = tmp_path / "textures"
    subdir = root / "sub"
    out_dir = tmp_path / "out"
    subdir.mkdir(parents=True)
    _write_png(root / "same.png", (1, 2, 3, 255))
    _write_png(subdir / "same.png", (4, 5, 6, 255))

    assert (
        cli_main(
            [
                "texture-convert",
                str(root),
                "--recursive",
                "--from-format",
                "png",
                "--to",
                "tga",
                "--output",
                str(out_dir),
            ]
        )
        == 0
    )

    root_tga = read_tga(io.BytesIO((out_dir / "same.tga").read_bytes()))
    nested_tga = read_tga(io.BytesIO((out_dir / "sub" / "same.tga").read_bytes()))
    assert root_tga.data[:4] == bytes((1, 2, 3, 255))
    assert nested_tga.data[:4] == bytes((4, 5, 6, 255))
