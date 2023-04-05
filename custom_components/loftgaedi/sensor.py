import json
import os
import logging
import requests
from datetime import timedelta
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
    
    def schedule_update(minute):
        now = datetime.now()
        update_time = now.replace(minute=minute, second=0, microsecond=0)
        if now >= update_time:
            update_time += timedelta(hours=1)
        track_time_change(hass, sensor.update, minute=20)

    schedule_update(20)

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
   
                  air_quality_labels = ["Óholl", "Óholl fyrir viðkvæma", "Sæmileg", "Góð", "Mjög góð"]                  
                  thresholds = pollutant_levels[pollutant]
                  air_quality = None
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
            