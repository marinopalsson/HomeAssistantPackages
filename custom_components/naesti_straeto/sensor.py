import logging
from datetime import timedelta, datetime
from homeassistant.helpers.entity import Entity
from homeassistant.util import Throttle
from .api import fetch_busstop_data, get_stop_name

_LOGGER = logging.getLogger(__name__)

DOMAIN = "naesti_straeto"
SCAN_INTERVAL = timedelta(minutes=1)

def setup_platform(hass, config, add_entities, discovery_info=None):
    busstop_id = config["busstop_id"]
    bus_line = config["bus_line"]
    stop_data_file_path = config["stop_data_file_path"]
    entities = []

    entities.append(BusstopSensor(busstop_id, bus_line,  stop_data_file_path))
    add_entities(entities, True)

class BusstopSensor(Entity):
    def __init__(self, busstop_id, bus_line, stop_data_file_path):
        self._busstop_id = busstop_id
        self._bus_line = bus_line
        self._state = None
        self._attributes = {}
        self._stop_name = get_stop_name(busstop_id, stop_data_file_path)
        self._destination = None

    @property
    def name(self):
        return f"Strætó {self._bus_line} {self._busstop_id}"

    @property
    def state(self):
        return self._state

    @property
    def icon(self):
        return "mdi:bus-clock"

    @property
    def unit_of_measurement(self):
        if self._state != "Enginn strætó á leiðinni":
            return "min"
        else:
            return None

    @property
    def extra_state_attributes(self):
        attrs = self._attributes.copy()
        attrs["stop_name"] = self._stop_name
        if "til" in self._attributes:
            attrs["destination"] = self._attributes["til"]
        if "koma" in self._attributes:
            attrs["arrival_time"] = self._attributes["koma"]
        return attrs

    @Throttle(SCAN_INTERVAL)
    def update(self):
        data = fetch_busstop_data(self._busstop_id)

        if data:
            komur = data["feeds"][0].get("komur", [])
            next_bus = None

            for bus in komur:
                if bus["leid"] == self._bus_line:
                    arrival_time = datetime.strptime(bus["koma"], "%H:%M").time()
                    now = datetime.now().time()

                    if next_bus is None or arrival_time < datetime.strptime(next_bus["koma"], "%H:%M").time():
                        time_difference = (datetime.combine(datetime.today(), arrival_time) - datetime.combine(datetime.today(), now)).seconds
                        if time_difference < 86400:  # Only consider buses arriving within the next 24 hours
                            next_bus = bus

            if next_bus:
                arrival_time = datetime.strptime(next_bus["koma"], "%H:%M")
                now = datetime.now()
                time_difference = (datetime.combine(datetime.today(), arrival_time.time()) - datetime.combine(datetime.today(), now.time())).seconds
                self._state = int(time_difference / 60)
                self._attributes = next_bus
            else:
                self._state = "Enginn strætó á leiðinni"
                self._attributes = {}
        else:
            _LOGGER.error("Failed to update bus stop data")
