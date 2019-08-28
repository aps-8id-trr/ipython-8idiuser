
"""
Ophyd support for the EPICS epid record


Public Structures

.. autosummary::
   
    ~epidRecord

:see: https://epics.anl.gov/bcda/synApps/std/epidRecord.html
"""

#-----------------------------------------------------------------------------
# :author:    Pete R. Jemian
# :email:     jemian@anl.gov
# :copyright: (c) 2017-2019, UChicago Argonne, LLC
#
# Distributed under the terms of the Creative Commons Attribution 4.0 International Public License.
#
# The full license is in the file LICENSE.txt, distributed with this software.
#-----------------------------------------------------------------------------

from ophyd.device import Device, Component
from ophyd import EpicsSignal, EpicsSignalRO
from .common_fields import EpicsRecordDeviceCommonAll
from .common_fields import EpicsRecordFloatFields


__all__ = ["epidRecord", ]


class epidRecord(EpicsRecordFloatFields, EpicsRecordDeviceCommonAll):
    """
    EPICS epid record support in ophyd
    
    :see: https://epics.anl.gov/bcda/synApps/std/epidRecord.html
    """
    proportional_gain = Component(EpicsSignal, ".KP")
    integral_gain = Component(EpicsSignal, ".KI")
    derivative_gain = Component(EpicsSignal, ".KD")

    following_error = Component(EpicsSignalRO, ".ERR")
    output_value = Component(EpicsSignalRO, ".OVAL")

    calculated_P = Component(EpicsSignalRO, ".P")
    calculated_I = Component(EpicsSignal, ".I")
    calculated_D = Component(EpicsSignalRO, ".D")

    clock_ticks = Component(EpicsSignalRO, ".CT")
    time_difference = Component(EpicsSignal, ".DT")

    # limits imposed by the record support:
    #     .LOPR <= .OVAL <= .HOPR
    #     .LOPR <= .I <= .HOPR
    high_limit = Component(EpicsSignal, ".DRVH")
    low_limit = Component(EpicsSignal, ".DRVL")

    @property
    def value(self):
        return self.output_value.value
