from homeassistant.helpers.entity import Entity
from homeassistant.const import STATE_ON, STATE_OFF
from datetime import datetime

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    fasce = []
    for fascia in [1, 2, 3]:
        for giorno in ['lunedi', 'martedi', 'mercoledi', 'giovedi', 'venerdi', 'sabato', 'domenica']:
            fasce.append(FasciaAttivaSensor(hass, fascia, giorno))
    async_add_entities(fasce)

class FasciaAttivaSensor(Entity):
    def __init__(self, hass, fascia, giorno):
        self._hass = hass
        self._fascia = fascia
        self._giorno = giorno
        self._name = f"Fascia {fascia} Attiva {giorno.capitalize()}"
        self._state = STATE_OFF

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        inizio = self._hass.states.get(f"input_datetime.fascia_{self._fascia}_{self._giorno}_inizio").state[:5]
        fine = self._hass.states.get(f"input_datetime.fascia_{self._fascia}_{self._giorno}_fine").state[:5]
        ora = datetime.now().strftime("%H:%M")
        if self._hass.states.get(f"input_boolean.fascia_{self._fascia}_abilitata").state == "on" and inizio <= ora <= fine:
            return STATE_ON
        return STATE_OFF
