from covid_planner import *
from datetime import datetime, timedelta


def main():
    place = 'Zurich'
    time = datetime.now() + timedelta(days=1)
    password = "Coffee"

    planner = CovidPlanner()
    planner.create_zoom_meeting(place=place, start_time=time, password=password)


if __name__ == "__main__":
    main()
