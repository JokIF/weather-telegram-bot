from aiohttp import ClientSession

from main_bot.middlewares import i18n
from .classes import LocalDate

from dataclasses import dataclass

from loguru import logger

_ = i18n.gettext


class GismeteoAPI:
    URL = "https://api.gismeteo.net/v2/weather/"

    def __init__(self, TOKEN):
        self._header = {"X-Gismeteo-Token": TOKEN}

        self.url_today_forcast = self.URL + "forecast/?latitude={lat}&longitude={lon}&days=2&lang={lang}"
        self.url_today = self.URL + "current/?latitude={lat}&longitude={lon}&lang={lang}"
        self.url_tomorrow = ""

    async def get_data(self, lat, lon, url, lang):
        async with ClientSession() as session:
            async with session.get(url=url.format(lat=lat, lon=lon, lang=lang),
                                   headers=self._header) as response:
                if response.status == 200:
                    return await response.json()
                err = await response.json()
                logger.exception(f"some thing wrong {err}")

    def parsing(self, json: dict, lang: str, main: bool = False):

        wind = str(json["wind"]["speed"]["m_s"]) + " " + _("m/s") + "\n" \
               + self._define_wind_direct(json["wind"]["direction"]["scale_8"])

        data = self.Data_(
            pressure=str(json["pressure"]["mm_hg_atm"]) + "\n" + _("mm Hg"),
            humidity=str(json["humidity"]["percent"]),
            wind=wind,
            precipitation=self._define_precipitation(json["precipitation"]["type"],
                                                     json["precipitation"]["intensity"]),
            precipitation_amount=json["precipitation"]["amount"],
            temperature=self._define_temperature(json["temperature"]["comfort"]["C"], main),
            temperature_water=self._define_temperature(json["temperature"]["water"]["C"], main),
            temperature_air=self._define_temperature(json["temperature"]["air"]["C"], main),
            description=json["description"]["full"],
            date=LocalDate(json["date"], lang, main),
            icon=self._define_icon(json["icon"])
        )

        return data

    @staticmethod
    def _define_icon(icon_name: str):
        logger.debug(icon_name)
        match icon_name.split("_"):
            case [*_, "st"]:
                return "st"
            case [*_, ("r1" | "r2" | "r3") as rain]:
                return rain
            case [*_, ("s1" | "s2" | "s3") as snow]:
                return snow
            case [*_, ("rs1" | "rs2" | "rs3") as rsnow]:
                return rsnow
            case [("d" | "n") as day_night, *something]:
                match something:
                    case [("c1" | "c2" | "c3") as cloud, *_]:
                        return f"{day_night}_{cloud}"
                    case _:
                        return day_night
            case ["c1" | "c2" | "c3" as cloud]:
                return cloud


    @staticmethod
    def _define_temperature(temper: int, main: bool):
        return f"{round(temper):+}" if main else f"{round(temper)}ºC"

    @staticmethod
    def _define_wind_direct(scale: int) -> str:
        match scale:
            case 0:
                return _("calm")
            case 1:
                return _("N ↑")
            case 2:
                return _("N-E ↗")
            case 3:
                return _("E →")
            case 4:
                return _("S-E ↘")
            case 5:
                return _("S ↓")
            case 6:
                return _("S-W ↙")
            case 7:
                return _("W ←")
            case 8:
                return _("N-W ↖")

    # -----------------------------
    # мб не нужно
    @staticmethod
    def _define_precipitation(type_: int, intensity: int):
        type_dict = {0: "No precipitation",
                     1: "rain",
                     2: "snow",
                     3: "Mixed rainfall"}
        intensity_dict = {1: "Small",
                          2: "",
                          3: "heavy"}

        if type_ == 3 or type_ == 0:
            return type_dict[type_]
        return f"{intensity_dict[intensity]} {type_dict[type_]}"

    # --------------------------------

    @dataclass
    class Data_:
        pressure: str
        humidity: str
        wind: str
        precipitation: str
        precipitation_amount: str
        temperature: str
        temperature_water: str
        temperature_air: str
        description: str
        date: LocalDate
        icon: str
