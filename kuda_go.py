import re
from dataclasses import dataclass, field
from typing import List
from abc import ABC, abstractmethod

import requests
from bs4 import BeautifulSoup


@dataclass
class ScheduleSession:
    time: str
    price: int


@dataclass
class FilmData:
    image_url: str
    title: str
    description: str = ''
    description_href: str = ''
    schedule: List[ScheduleSession] = field(default_factory=set)


class KudaGoApi:
    KUDAGO_HOST = "https://kudago.com"

    def _send_api_request(self, endpoint):
        return requests.get(f'{self.KUDAGO_HOST}{endpoint}')

    def get_recent_films(self):
        response = self._send_api_request("/msk/kino/schedule-cinema")

        soup = BeautifulSoup(response.text, features="html.parser")
        film_list = soup.find_all('article', {'class': 'post post-rect'})

        films = []
        for film in film_list:
            image_url = film.find('div', {'class': 'post-image-src'}).get('data-echo-background')
            image_url = f'{self.KUDAGO_HOST}{image_url}'

            title = film.find('a', {'class': 'post-title-link'}).get('title')

            description = film.find('div', {'class': 'post-description'}).contents
            description = description[0].replace('\n', '')
            description = description.strip()
            films.append(FilmData(image_url, title, description))

        return films


class BaseAPI(ABC):
    HOST = ''

    def _send_api_request(self, endpoint: str):
        return requests.get(f'{self.HOST}{endpoint}')

    @abstractmethod
    def get_recent_films(self) -> List[FilmData]:
        pass


class KapitoliyAPI(BaseAPI):
    HOST = 'http://www.nescafe-imaxcinema.ru'

    def get_recent_films(self):
        response = self._send_api_request("/timetable/")

        soup = BeautifulSoup(response.text, features="html.parser")
        film_list = soup.find_all('div', {'class': 'movie clearfix'})

        films = []
        for film in film_list:
            title = film.find('a', {'class': 'name'}).contents()[0].strip()
            description_href = film.find('a', {'class': 'name'}).get('href')

            response_description = self._send_api_request('/description_href/')
            description_href = f'{self.HOST}{description_href}'

            soup_description = BeautifulSoup(response_description.text, features="html.parser")
            description = soup_description.find('div', {'class': 'description'}).contents[0].strip()

            image_url = soup_description.find('div', {'class': 'cover'}).find('img').get('src')

            films.append(FilmData(image_url,
                                  title,
                                  schedule=schedule_sessions,
                                  description_href=description_href,
                                  description=description))

            schedule_session = []
            sessions = film.find_all('div', {'class': 'time clearfix'})

            for session in sessions:
                session_time = session.find('span', {'class': 'shedule_session_time'}).contents[0].strip()

                session_price = session.find('span', {'class': 'shedule_session_price'}).contents[0].strip()
                session_price = int(re.search(r'\d+', session_price).group())

        return films


class MetropolisAPI(BaseAPI):
    HOST = "https://kinoteatr.ru"

    def get_recent_films(self) -> List[FilmData]:
        response = self._send_api_request("/raspisanie-kinoteatrov/metropolis/")

        soup = BeautifulSoup(response.text, features="html.parser")
        film_list = soup.find_all('div', {'class': 'shedule_movie bordered gtm_movie'})

        films = []
        for film in film_list:
            image_url = film.find('img', {'class': 'shedule_movie_img'}).get('src')
            title = film.get('data-gtm-list-item-filmname')
            description_href = film.find('a', {'class': 'gtm-ec-list-item-movie'}).get('href')

            response_description = requests.get(description_href)
            soup_description = BeautifulSoup(response_description.text, features="html.parser")
            description = soup_description.find('p', {'class': 'movie_card_description_inform'}).contents[0].strip()

            schedule_sessions = []
            sessions = film.find_all('a', {'class': 'shedule_session'})

            for session in sessions:
                session_time = session.find('span', {'class': 'shedule_session_time'}).contents[0].strip()

                session_price = session.find('span', {'class': 'shedule_session_price'}).contents[0].strip()
                session_price = int(re.search(r'\d+', session_price).group())

                schedule_sessions.append(ScheduleSession(session_time, session_price))

            films.append(FilmData(image_url,
                                  title,
                                  schedule=schedule_sessions,
                                  description_href=description_href,
                                  description=description))
        return films


if __name__ == '__main__':
    metr = MetropolisAPI()
    metr.get_recent_films()
