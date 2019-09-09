logger.info(__file__)

"""detectors (area detectors handled separately)"""

class LocalScalerCH(ScalerCH):
    
    def staging_setup_DM(self, *args, **kwargs):
        """
        setup the scaler's stage_sigs for acquisition with the DM workflow

        Implement this method in _any_ Device that requires custom
        setup for the DM workflow.
        """
        assert len(args) == 1
        acquire_period = args[0]
        self.stage_sigs["count_mode"] = "AutoCount"
        self.stage_sigs["auto_count_time"] = max(0.1,acquire_period)


scaler1 = LocalScalerCH('8idi:scaler1', name='scaler1', labels=["scalers", "detectors"])

_timeout = time.time() + 10
while time.time() < _timeout:
    if scaler1.connected:
        break
    time.sleep(0.2)
if time.time() > _timeout:
    msg = "10s timeout expired waiting for scaler1 to connect"
    raise RuntimeError(msg)
del _timeout

scaler1.select_channels(None)   # choose just the channels with EPICS names

# TODO: like IOMon, do for the other channels in use
# note that the chan=# is zero-based  so add 1 for scaler1 channel object name

# This configuration moved from 15-spec-config.py
# counter: sec = SpecCounter(mne='sec', config_line='0', name='Seconds', unit='0', chan='0', pvname=8idi:scaler1.S1)
# counter: pind1 = SpecCounter(mne='pind1', config_line='1', name='pind1', unit='0', chan='1', pvname=8idi:scaler1.S2)
# counter: I0Mon = SpecCounter(mne='I0Mon', config_line='2', name='I0Mon', unit='0', chan='7', pvname=8idi:scaler1.S8)
I0Mon = scaler1.channels.chan08.s
# counter: pind2 = SpecCounter(mne='pind2', config_line='3', name='pind2', unit='0', chan='2', pvname=8idi:scaler1.S3)
# counter: pind3 = SpecCounter(mne='pind3', config_line='4', name='pind3', unit='0', chan='3', pvname=8idi:scaler1.S4)
# counter: pind4 = SpecCounter(mne='pind4', config_line='5', name='pind4', unit='0', chan='4', pvname=8idi:scaler1.S5)
# counter: pdbs = SpecCounter(mne='pdbs', config_line='6', name='pdbs', unit='0', chan='5', pvname=8idi:scaler1.S6)
# counter: I_APS = SpecCounter(mne='I_APS', config_line='7', name='I_APS', unit='0', chan='6', pvname=8idi:scaler1.S7)
# line 8: CNT008 =     NONE  2  0      1 0x000     ccdc  ccdc
Atten1 = EpicsSignalRO('8idi:userTran1.P', name='Atten1', labels=["detectors",])
Atten2 = EpicsSignalRO('8idi:userTran3.P', name='Atten2', labels=["detectors",])
att1 = EpicsSignal('8idi:BioDecode1.A', name='att1', write_pv='8idi:BioEncode1.A')
att2 = EpicsSignal('8idi:BioDecode2.A', name='att2', write_pv='8idi:BioEncode2.A')


T_A = EpicsSignalRO('8idi:LS336:TC4:IN1', name='T_A', labels=["detectors",])
T_SET = EpicsSignalWithRBV('8idi:LS336:TC4:OUT1:SP', name='T_SET', labels=["detectors",])
# counter: APD = SpecCounter(mne='APD', config_line='13', name='APD', unit='0', chan='8', pvname=8idi:scaler1.S9)
