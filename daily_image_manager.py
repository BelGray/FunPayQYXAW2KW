import json
import os.path
from aiogram.types import File

from loader import bot


class DailyImage:
    __json_file_name = "image.json"
    __path = "images/"

    @staticmethod
    async def init_json():
        if not os.path.exists(DailyImage.__path):
            os.mkdir(DailyImage.__path)
        if not os.path.exists(DailyImage.__json_file_name):
            with open(DailyImage.__json_file_name, "w") as writer:
                writer.write("{}")
                writer.close()
            with open(DailyImage.__json_file_name, "r") as file:
                data = json.load(file)
                file.close()
            with open(DailyImage.__json_file_name, "w") as data_writer:
                data["image_path"] = None
                json.dump(data, data_writer)
                data_writer.close()

    @staticmethod
    async def remove_current_path():
        await DailyImage.init_json()
        path = await DailyImage.get_path()
        if path is not None:
            if await DailyImage.exists(path):
                os.remove(path)
                with open(DailyImage.__json_file_name, "r") as file:
                    data = json.load(file)
                    file.close()
                with open(DailyImage.__json_file_name, "w") as data_writer:
                    data["image_path"] = None
                    json.dump(data, data_writer)
                    data_writer.close()


    @staticmethod
    async def save(file_path: File):
        await DailyImage.init_json()
        path = DailyImage.__path + file_path.file_path.split("/")[-1]
        await bot.download_file(file_path.file_path, destination=path)
        with open(DailyImage.__json_file_name, "r") as file:
            data = json.load(file)
            file.close()
        with open(DailyImage.__json_file_name, "w") as data_writer:
            data["image_path"] = path
            json.dump(data, data_writer)
            data_writer.close()

    @staticmethod
    async def exists(path: str) -> bool:
        return os.path.exists(path)

    @staticmethod
    async def get_path() -> str:
        await DailyImage.init_json()
        with open(DailyImage.__json_file_name, "r") as file:
            data = json.load(file)
            file.close()
        return str(data["image_path"])
