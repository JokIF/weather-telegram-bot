from aiogram import types

from sqlalchemy.sql.expression import desc

from main_bot import config
from main_bot.database import LocationUser, UserImages
from main_bot.init import dp, gismeteo
from main_bot.filters import WeatherCurrentWord
from main_bot.utils.handls_keyboards import keyboard_weather_current, keyboard_weather_current_cancel
from main_bot.utils import WeatherStates

import datetime


async def all_user_images(user_id: int):
    desc_obj = desc(UserImages.create_at)
    return await UserImages.query.where(
        UserImages.user_id == user_id).order_by(desc_obj).gino.all()


@dp.message_handler(WeatherCurrentWord())
async def weather_current(message: types.Message, user_loc: LocationUser, locale: str):
    await message.answer_chat_action(types.ChatActions.UPLOAD_PHOTO)
    all_images = await all_user_images(user_loc.user_id)
    available_requests = list(image for image in all_images
                              if (datetime.datetime.utcnow() - image.create_at).days != 0)

    if len(all_images) > 9 and available_requests:
        await all_images[-1].delete()

    await WeatherStates.current_weather.set()

    if available_requests or len(all_images) < 4:
        url = await gismeteo.draw_image_today(user_loc.lat,
                                              user_loc.lon,
                                              user_loc.address,
                                              locale,
                                              config.USERS_IMGS)
        await UserImages.create(user_id=user_loc.user_id,
                                url=str(url),
                                create_at=datetime.datetime.utcnow())

        return_ = []
        with open(url, "rb") as photo:
            return_.append(await message.answer_photo(photo=photo))

        text, inline = keyboard_weather_current()
        return_.append(await message.answer(text=text, reply_markup=inline))
        return return_
    text, inline = keyboard_weather_current_cancel()
    return await message.answer(text=text, reply_markup=inline)
