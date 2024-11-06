"""Free@Home ForceOnOffSensor Class."""

from typing import Any

from ..api import FreeAtHomeApi
from ..bin.pairing import Pairing
from .base import Base


class ForceOnOffSensor(Base):
    """Free@Home ForceOnOffSensor Class."""

    _state_refresh_output_pairings: list[Pairing] = [
        Pairing.AL_FORCED,
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
        """Initialize the Free@Home ForceOnOffSensor class."""
        self._state: bool | None = None

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
        """Get the forceOnOff state."""
        return self._state

    def _refresh_state_from_output(self, output: dict[str, Any]) -> bool:
        """
        Refresh the state of the device from a given output.

        This will return whether the state was refreshed as a boolean value.
        """
        if output.get("pairingID") == Pairing.AL_FORCED.value:
            """
            If the rocker is configured as 'force on':
            3 means on
            1 means off
            If the rocker is configured as 'force off':
            2 means on
            0 means off
            """
            self._state = output.get("value") in ("2", "3")
            return True
        return False