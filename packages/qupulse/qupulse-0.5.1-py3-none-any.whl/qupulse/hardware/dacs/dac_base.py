from abc import ABCMeta, abstractmethod
from typing import Dict, Tuple, Iterable

import numpy

__all__ = ['DAC']


class DAC(metaclass=ABCMeta):
    """Representation of a data acquisition card"""

    @abstractmethod
    def register_measurement_windows(self, program_name: str, windows: Dict[str, Tuple[numpy.ndarray,
                                                                                       numpy.ndarray]]) -> None:
        """"""

    @abstractmethod
    def set_measurement_mask(self, program_name, mask_name, begins, lengths) -> Tuple[numpy.ndarray, numpy.ndarray]:
        """returns length of windows in samples"""

    @abstractmethod
    def register_operations(self, program_name: str, operations) -> None:
        """"""
    
    @abstractmethod
    def arm_program(self, program_name: str) -> None:
        """"""

    @abstractmethod
    def delete_program(self, program_name) -> None:
        """"""

    @abstractmethod
    def clear(self) -> None:
        """Clears all registered programs.

        Caution: This affects all programs and waveforms on the AWG, not only those uploaded using qupulse!
        """

    @abstractmethod
    def measure_program(self, channels: Iterable[str]) -> Dict[str, numpy.ndarray]:
        """Get the last measurement's results of the specified operations/channels"""
