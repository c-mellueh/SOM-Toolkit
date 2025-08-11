from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from . import ui
LENGTH_UNITS = []
AREA_UNITS = []
VOLUME_UNITS = []
MASS_UNITS = []
TIME_UNITS = []
ENERGY_UNITS = []
COUNT_UNITS = []
TEMPERATURE_UNITS = []

UNITS = {
    "Length": LENGTH_UNITS,
    "Area": AREA_UNITS,
    "Volume": VOLUME_UNITS,
    "Energy": ENERGY_UNITS,
    "Temperature": TEMPERATURE_UNITS,
    "Mass": MASS_UNITS,
    "Time": TIME_UNITS,
    "Counting": COUNT_UNITS,
}


class UnitsProperties:
    unit_settings_widget: ui.UnitSettings | None = None
