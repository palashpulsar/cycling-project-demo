## Pace Strategy

This is a Django-based web-application designed for cycling coaches. In this application, a coach can upload a route (GPX format), and implant his/her voice instruction over the route. When a cyclist arrives over a point, he/she hears the instruction of the coach.

## Background of the project

This project was a part of [Servoped Oy](http://servoped.com), a Finnish company. A demo version of Pace Strategy was prepared to show the product to coaches.

Servoped later decided to switch its focus to bigger and lucrative automotive market, and hence this project was scrapped.

## Built With

* [Django](https://www.djangoproject.com) - The web framework used.
* [D3.js](https://d3js.org) - For graphical visualisation of data.
* Python version 2.7 is used for backend programming.

## Quick start
Create a virtual environment:
```
pip install virtualenv
virtualenv venv
source venv/bin/activate
```
Once the virtual environment is activated, install dependencies with
```
pip install -r requirements.txt
```

Download the project from GitHub with:
```
git clone https://github.com/palashpulsar/cycling-project-demo.git
```

Go to the project and run the development server as follows:
```
cd cycling-project-demo
python manage.py migrate
python manage.py runserver
```

The app utilizes [Strava API](https://strava.github.io/api/) for login. Strava is a popular application among athletes to track their activities. As a coach, go to the URL for Strava login:
```
127.0.0.1:8000/coach/login/
```
In case if you do not have Strava credential, you can use my login credential :)
```
Your Email: palash.servoped@gmail.com
Password: Pace-Strategy
```

In the following page, upload a route. There are three routes (or GPX files) under [GPX folder](/GPX folder/) that can be used for demonstation. Once the route is uploaded, it is displayed on a Google map, and a [D3.js](https://d3js.org) plot of distance vs elevation is shown.

A coach clicks on this D3js plot and record his/her voice instruction. In the backend side, [PyAudio](https://people.csail.mit.edu/hubert/pyaudio/) is activated to record and play the sound.


