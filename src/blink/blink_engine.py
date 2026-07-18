"""
Blink Engine
------------
Processes Eye Aspect Ratio (EAR) values and detects
short and long blinks.
"""

from enum import Enum
import time

from utils.config import (
    EAR_THRESHOLD,
    SHORT_BLINK_MAX,
    LONG_BLINK_MIN,
)


class BlinkEvent(Enum):
    NONE = 0
    SHORT_BLINK = 1
    LONG_BLINK = 2


class BlinkEngine:
    """
    Blink detection state machine.
    """

    def __init__(self):

        self.eye_closed = False
        self.closed_start_time = None

    def update(self, ear):
        """
        Update the blink engine with the latest EAR value.

        Parameters
        ----------
        ear : float
            Eye Aspect Ratio.

        Returns
        -------
        BlinkEvent
        """

        current_time = time.time()

        # Eye closes
        if not self.eye_closed and ear < EAR_THRESHOLD:

            self.eye_closed = True
            self.closed_start_time = current_time

            return BlinkEvent.NONE

        # Eye opens again
        if self.eye_closed and ear >= EAR_THRESHOLD:

            self.eye_closed = False

            duration = current_time - self.closed_start_time

            if duration < SHORT_BLINK_MAX:
                return BlinkEvent.SHORT_BLINK

            if duration >= LONG_BLINK_MIN:
                return BlinkEvent.LONG_BLINK

        return BlinkEvent.NONE