from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

import datetime
from dataclasses import dataclass
from itertools import dropwhile
from typing import Tuple
from uuid import uuid4

from ... import config
from .gismeteo_API import GismeteoAPI

from loguru import logger


class GismeteoDraw:
    _low_text_start = (358, 825)
    _low_text_size = 36
    _klein_thin, _kleinC_thin = map(str, config.assets_dir.glob("*.ttf"))
    _low_img_size = (166, 166)
    _main_img_size = (189, 189)
    _main_img_coords = (619, 326)
    _main_temperature_coords = (619, 348)
    _main_wind_direction_coords = (783, 688)
    _city_coords = (570, 204)
    _main_data_coords = (340, 637)
    _top_right_coords = (986, 96)

    def __init__(self, TOKEN):
        self._API: GismeteoAPI = GismeteoAPI(TOKEN)
        self._cursor = self._Cursor()

    async def draw_image_today(self, lat: int, lon: int, city: str, lang: str, outdir: Path):
        # raw_data_today = await self._API.get_data(lat, lon, self._API.url_today, lang)
        raw_data_forcast = await self._API.get_data(lat, lon, self._API.url_today_forcast, lang)
        data = self._filter_raw_data(raw_data_forcast, lang)

        with Image.open(config.assets_dir / "template.png") as templ:
            blank_frame = Image.new("RGBA", size=templ.size)

            self._main_text(data[0], blank_frame, city)  # main text

            # top right text
            for step, text in enumerate([data[0].date.time,
                                         data[0].date.date,
                                         data[0].date.weekday]):
                coords = (self._top_right_coords[0],
                          self._top_right_coords[1] + 40 * step)
                self._top_right(text, blank_frame, coords)

            # low text
            for step, short_data in enumerate(data[-3:]):
                coords = (self._low_text_start[0] + 172 * step,
                          self._low_text_start[1])
                self._low_text(short_data, blank_frame, coords)

            # create image
            out = Image.alpha_composite(templ, blank_frame)
            user_img_path = outdir / (str(uuid4()).replace('-', '_') + ".png")
            out.save(user_img_path, "PNG")
            out.close()

        return user_img_path

    def _filter_raw_data(self, raw_data: dict, lang: str):
        tz = raw_data["response"][0]["date"]["time_zone_offset"]
        now = datetime.datetime.utcnow() + datetime.timedelta(minutes=tz)
        raw_data = list(dropwhile(lambda d:
                                  (now - datetime.datetime.fromisoformat(
                                      d["date"]["local"])).seconds > 10800, raw_data["response"]))
        data = [self._API.parsing(raw_data[0], lang, True)]
        data.extend([self._API.parsing(d, lang) for d in raw_data[1:4]])
        return data

    def _low_text(self, short_data: GismeteoAPI.Data_,
                  blank_frame: Image.Image,
                  coords: Tuple[int, int]):
        self._cursor.coords = coords
        low_img_size: Tuple[int, int] = self._low_img_size
        fnt_time = ImageFont.truetype(self._klein_thin, self._low_text_size)
        fnt_tempare = ImageFont.truetype(self._kleinC_thin, self._low_text_size)
        draw = ImageDraw.ImageDraw(blank_frame)
        logger.debug(f"start {self._cursor.coords}")
        draw.text(xy=self._cursor.coords,
                  text=short_data.date.time,
                  fill="black",
                  font=fnt_time,
                  anchor="mb")
        logger.debug(short_data.icon)
        icon = Image.open(
            fp=next((config.assets_dir / "icons").glob(f"{short_data.icon}.png"))
        )
        icon = icon.resize(size=low_img_size)

        half_img_size = low_img_size[0] // 2
        box_par_1 = self._cursor - (half_img_size, 0)
        logger.debug(self._cursor.coords)
        box_par_2 = self._cursor + low_img_size
        logger.debug(self._cursor.coords)

        blank_frame.paste(im=icon,
                          box=(*box_par_1, *box_par_2)
                          )
        icon.close()
        draw.text(xy=self._cursor + (-1 * half_img_size, 0),
                  text=short_data.temperature,
                  font=fnt_tempare,
                  fill="black",
                  anchor="mt")
        logger.debug(self._cursor.coords)

    def _main_text(self, data: GismeteoAPI.Data_,
                   blank_frame: Image.Image,
                   city: str):
        draw = ImageDraw.ImageDraw(blank_frame)
        fnt_tempar = ImageFont.truetype(self._klein_thin, 165)
        fnt_city = ImageFont.truetype(self._klein_thin, 36)
        fnt_data = ImageFont.truetype(self._klein_thin, 30)
        self._cursor.coords = self._main_img_coords
        logger.debug(data.icon)
        icon = Image.open(
            fp=next((config.assets_dir / "icons").glob(f"{data.icon}.png"))
        )
        icon = icon.resize(size=self._main_img_size)  # x = 149 y = 129

        box_par_1 = self._cursor.coords
        box_par_2 = self._cursor + self._main_img_size
        logger.debug(f"{*box_par_1, *box_par_2}, {box_par_1}, {box_par_2}")

        blank_frame.paste(im=icon,
                          box=(*box_par_1, *box_par_2)
                          )
        icon.close()
        draw.text(xy=self._city_coords,
                  text=city,
                  fill="black",
                  font=fnt_city,
                  anchor="mt")
        draw.text(xy=self._main_temperature_coords,
                  text=data.temperature,
                  fill="black",
                  font=fnt_tempar,
                  anchor="rt")
        draw.text(xy=self._cursor.set(self._main_data_coords),
                  text=data.humidity + "%",
                  fill="black",
                  font=fnt_data,
                  anchor="mt")
        draw.multiline_text(xy=self._cursor + (190, 0),
                            text=data.pressure,
                            fill="black",
                            font=fnt_data,
                            align="center",
                            anchor="ma")
        draw.multiline_text(xy=self._cursor + (210, 0),
                            text=data.wind,
                            fill="black",
                            font=fnt_data,
                            align="center",
                            anchor="ma")

    def _top_right(self, data: str,
                   blank_frame: Image.Image,
                   coords: Tuple[int, int]):
        fnt = ImageFont.truetype(self._kleinC_thin, 26)
        draw = ImageDraw.ImageDraw(blank_frame)
        draw.text(xy=coords,
                  text=data,
                  fill="black",
                  font=fnt,
                  anchor="rb")

    @dataclass
    class _Cursor:
        x: int = 0
        y: int = 0

        def __add__(self, other):
            self.x += other[0]
            self.y += other[1]
            self.x = 0 if self.x < 0 else self.x
            self.y = 0 if self.y < 0 else self.y
            return self.x, self.y

        def __sub__(self, other):
            self.x -= other[0]
            self.y -= other[1]
            self.x = 0 if self.x < 0 else self.x
            self.y = 0 if self.y < 0 else self.y
            return self.x, self.y

        def set(self, _tuple: tuple):
            self.x, self.y = _tuple
            return self.x, self.y

        @property
        def coords(self):
            return self.x, self.y

        @coords.setter
        def coords(self, _tuple: tuple):
            self.x, self.y = _tuple
