import sys
import os
import shutil
import jwt
import requests
import json
import warnings
from pyowm import OWM
from pyowm.weatherapi25.weather_manager import WeatherManager
from datetime import datetime
from time import time
from typing import Final, Dict
from os.path import join as pjoin
from os.path import dirname as pdirname

from .utils import emoji_print

import yaml

__all__ = ["CovidPlanner"]

ZoomKeyContents = Dict[str, Dict[str, str]]  # todo make recursive as soon as mypy supports it


class CovidPlanner:
    # constants:
    _CONFIG_FILE_DIR: Final[str] = pjoin(pdirname(pdirname(pdirname(__file__))), "config")
    _TEMPLATE_FILE_DIR: Final[str] = pjoin(pdirname(__file__), "templates")
    _API_KEY_FILE: Final[str] = "api_keys.yaml"
    _API_KEY_TEMPLATE_FILE: Final[str] = "api_keys_template.yaml"

    api_key_file_path: str
    _owm: OWM
    _weather_manager: WeatherManager

    def __init__(self):
        self.api_key_file_path: str = pjoin(self._CONFIG_FILE_DIR, self._API_KEY_FILE)

        if not os.path.isfile(self.api_key_file_path):

            if not os.path.isdir(self._CONFIG_FILE_DIR):
                os.mkdir(self._CONFIG_FILE_DIR)

            shutil.copy(pjoin(self._TEMPLATE_FILE_DIR, self._API_KEY_TEMPLATE_FILE), self.api_key_file_path)
            sys.stdout.write(
                f"No API Key File found. New one is generated in {self.api_key_file_path}."
                f"\nPlease fill out the contents as specified in the README.md and restart the program.")
            exit(0)

        self._owm = OWM(self._owm_key)
        self._weather_mgr = self._owm.weather_manager()

    def create_zoom_meeting(self, place: str, start_time: datetime = datetime.now(), password: str = "coffee"):

        # todo: create GUI and pass as user inputs

        if self._is_rainy_at(place, start_time):
            # todo: creat wind and temperature check
            emoji_print("It is raining go meet on zoom :disappointed_face:")
            self._create_zoom_meeting(start_time, password)
        else:
            emoji_print("Go meet outside, it's not raining :grinning_face_with_big_eyes:!")

        # todo: send mail to everybody

    def _create_zoom_meeting(self, start_time: datetime, password: str):
        # todo: make user configurable
        meeting_details = {"topic": "Coffee Break",
                           "type": 2,
                           "start_time": f"{start_time}",
                           "duration": "45",
                           "timezone": "Europe/Zurich",

                           "recurrence": {"type": 1,
                                          "repeat_interval": 1
                                          },
                           "settings": {"host_video": "true",
                                        "participant_video": "true",
                                        "join_before_host": "true",
                                        "mute_upon_entry": "False",
                                        "watermark": "true",
                                        "audio": "voip",
                                        "auto_recording": "cloud"
                                        },
                           "password": password  # fixme: how to remove password?
                           }
        headers = {'authorization': f'Bearer {self._generate_token()}',
                   'content-type': 'application/json'}
        r = requests.post(
            f'https://api.zoom.us/v2/users/me/meetings',
            headers=headers, data=json.dumps(meeting_details))

        print("creating zoom meeting...\n")
        # print(r.text)
        # converting the output into json and extracting the details
        y = json.loads(r.text)
        join_url = y["join_url"]
        meeting_password = y["password"]

        print(
            f'here is your zoom meeting link {join_url} and your password: "{meeting_password}".\n')

    def _generate_token(self) -> str:
        token = jwt.encode(

            # Create a payload of the token containing
            # API Key & expiration time
            {'iss': self._zoom_key, 'exp': time() + 5000},

            # Secret used to generate token signature
            self._zoom_secret,

            # Specify the hashing alg
            'HS256'
        )
        return token

    def _is_rainy_at(self, place: str, time_to_check: datetime) -> bool:
        forecast = self._weather_mgr.forecast_at_place(place, '3h')  # give where you need to see the weather
        if time_to_check.astimezone() < forecast.when_starts('date'):
            warnings.warn(f"Time to smaller than start of forecast, using {forecast.when_starts('date')} instead.")
            _time = forecast.when_starts('date')
        elif time_to_check.astimezone() > forecast.when_ends('date'):
            warnings.warn(f"Time to bigger than end of forecast, using {forecast.when_ends('date')} instead")
            _time = forecast.when_ends('date')
        else:
            _time = time_to_check
        is_rainy = forecast.will_be_rainy_at(_time.astimezone())
        return is_rainy

    @property
    def _zoom_secret(self) -> str:
        yaml_contents = self._load_key_file()
        return yaml_contents["Zoom"]["Secret"]

    @property
    def _zoom_key(self) -> str:
        yaml_contents = self._load_key_file()
        return yaml_contents["Zoom"]["Key"]

    @property
    def _owm_key(self):
        yaml_contents = self._load_key_file()
        return yaml_contents["OpenWeatherMap"]["Key"]

    def _load_key_file(self) -> ZoomKeyContents:
        with open(self.api_key_file_path) as yaml_file:
            yaml_contents = yaml.full_load(yaml_file)
        return yaml_contents
