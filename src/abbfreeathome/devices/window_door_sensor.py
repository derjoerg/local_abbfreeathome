"""Free@Home WindowDoorSensor Class."""

import enum
from typing import Any

from ..api import FreeAtHomeApi
from ..bin.pairing import Pairing
from .base import Base


class WindowDoorSensorPosition(enum.Enum):
    """
    An Enum class for window/door sensor possible positions.

    Home Assistant requires the name to be all lowercase.
    """

    unknown = None
    closed = "0"
    tilted = "33"
    open = "100"


class WindowDoorSensor(Base):
    """Free@Home WindowDoorSensor Class."""

    _state_refresh_pairings: list[Pairing] = [
        Pairing.AL_WINDOW_DOOR,
    ]
    _callback_attributes: list[str] = [
        "state",
        "position",
    ]

    def __init__(
        self,
        device_id: str,
        device_name: str,
        channel_id: str,
        channel_name: str,
        inputs: dict[str, dict[str, Any]],
        outputs: dict[str, dict[str, Any]],
        parameters: dict[str, dict[str, Any]],
        api: FreeAtHomeApi,
        floor_name: str | None = None,
        room_name: str | None = None,
    ) -> None:
        """Initialize the Free@Home WindowDoorSensor class."""
        self._state: bool | None = None
        self._position: WindowDoorSensorPosition = WindowDoorSensorPosition.unknown

        super().__init__(
            device_id,
            device_name,
            channel_id,
            channel_name,
            inputs,
            outputs,
            parameters,
            api,
            floor_name,
            room_name,
        )

    @property
    def state(self) -> bool | None:
        """Get the sensor state."""
        return self._state

    @property
    def position(self) -> str | None:
        """Get the sensor position."""
        return self._position.name

    def _refresh_state_from_datapoint(self, datapoint: dict[str, Any]) -> str:
        """
        Refresh the state of the device from a given output.

        This will return whether the state was refreshed as a boolean value.
        """
        if datapoint.get("pairingID") == Pairing.AL_WINDOW_DOOR.value:
            self._state = datapoint.get("value") == "1"
            return "state"
        if datapoint.get("pairingID") == Pairing.AL_WINDOW_DOOR_POSITION.value:
            try:
                self._position = WindowDoorSensorPosition(datapoint.get("value"))
            except ValueError:
                self._position = WindowDoorSensorPosition.unknown
            return "position"
        return None
