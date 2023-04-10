import json
import os
import logging
import requests
from datetime import datetime, timedelta
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.event import track_time_change
from homeassistant.const import CONF_NAME

_LOGGER = logging.getLogger(__name__)

# Load pollutant levels from JSON file
with open(os.path.join(os.path.dirname(__file__), "pollutant_levels.json")) as f:
    pollutant_levels = json.load(f)

def setup_platform(hass, config, add_entities, discovery_info=None):
    station_id = config["station_id"]
    name = config.get(CONF_NAME, "Loftgaedi")
    sensor = LoftgaediSensor(station_id, name)
    add_entities([sensor], True)

def get_air_quality_label(pollutant, value, pollutant_levels):
    levels = pollutant_levels[pollutant]
    for level in levels:
        if "max_value" not in level or value <= level["max_value"]:
            return level["label"]
    return "Unknown"

class LoftgaediSensor(Entity):
    def __init__(self, station_id, name):
        self._station_id = station_id
        self._name = name
        self._state = None
        self._attributes = {}
        self._last_update_hour = datetime.now().replace(minute=0, second=0, microsecond=0)
        self._updated_this_hour = False
        self._first_update_done = False
        
    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state

    @property
    def icon(self):
        return "mdi:weather-windy-variant"

    @property
    def extra_state_attributes(self):
        return self._attributes

    def update(self):
        now = datetime.now()
        current_hour = now.replace(minute=0, second=0, microsecond=0)

        if not self._first_update_done or (now.minute == 20 and now.second < 30 and not self._updated_this_hour):
            self._first_update_done = True
            self._updated_this_hour = True
        
            _LOGGER.info(f"Fetching loftgæði data for {self._station_id} ")
            url = f"https://api.ust.is/aq/a/getCurrent/id/{self._station_id}"
            response = requests.get(url)
            data = response.json()

            pollutants_of_interest = {"PM2.5", "PM10", "NO2", "SO2", "H2S"}

            highest_pollutant_level = None
            highest_pollutant_level_index = None

            if self._station_id in data:
                station_data = data[self._station_id]["parameters"]

                for pollutant, pollutant_data in station_data.items():
                    if pollutant in pollutants_of_interest:
                        latest_data = pollutant_data["0"]
                        styrkur = float(latest_data["value"])
                        timi = latest_data["endtime"]
                        mælieining = pollutant_data["unit"].replace('\\', '')
                        valid = latest_data["verification"] == 3

                        air_quality_labels = ["Óholl", "Óholl fyrir viðkvæma", "Sæmileg", "Góð", "Mjög góð"]                  
                        thresholds = pollutant_levels[pollutant]
                        air_quality = None
                        if valid:
                            for index, threshold in enumerate(thresholds):
                                if styrkur >= threshold:
                                    air_quality = air_quality_labels[index]
                                    break
                                
                        if air_quality is None:
                            air_quality = air_quality_labels[-1]

                        self._attributes[f"{pollutant}_loftgæði"] = air_quality
                        self._attributes[f"{pollutant}_styrkur"] = styrkur
                        self._attributes[f"{pollutant}_mælieining"] = mælieining
                        self._attributes[f"{pollutant}_tími"] = timi
                        self._attributes[f"{pollutant}_mæling"] = "gild" if valid else "ógild"

                        if valid:
                            # Find the index of the current air_quality_label
                            current_pollutant_level_index = air_quality_labels.index(air_quality)

                            # Compare the current index to the highest index found so far
                            if highest_pollutant_level_index is None or current_pollutant_level_index < highest_pollutant_level_index:
                                highest_pollutant_level_index = current_pollutant_level_index
                                highest_pollutant_level = air_quality

                self._state = highest_pollutant_level
            else:
                _LOGGER.error(f"Station {self._station_id} not found in API response.")
                self._state = "Error"
        elif self._last_update_hour != now.replace(minute=0, second=0, microsecond=0):
            self._last_update_hour = now.replace(minute=0, second=0, microsecond=0)
            self._updated_this_hour = False
