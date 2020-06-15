logger.info(__file__)

"""
local, custom Device definitions

DEVICES

    BeamSplittingMonochromatorDevice()
    BeWindow()
    CompoundRefractiveLensDevice()
    DetStageDownstream()
    DetStageUpstream()
    FlightPathTable()
    FOEmirrorDevice()
    FOEpinholeDevice()
    LS336Device()
    MonochromatorDevice()
    MonochromatorTableDevice()
    PreampDevice()
    PreampUnitNumberDevice()
    PSO_TaxiFly_Device()
    PSS_Parameters()
    #SamplePiezo()
    SampleStage()
    SampleStageTable()
    ShutterStage()
    SlitI1Device()
    SlitI2Device()
    SlitI3Device()
    SlitI4Device()
    SlitI5Device()
    SlitIpinkDevice()
    SoftGlueDevice()
    TableOptics()
    WBslitDevice()
"""


class CompoundRefractiveLensDevice(Device):
    x = Component(EpicsMotor, '8idi:m65', labels=["motor", "crl", "optics"])
    # y = Component(EpicsMotor, '8idi:m68', labels=["motor", "crl", "optics"])
    z = Component(EpicsMotor, '8idi:m62', labels=["motor", "crl", "optics"])
    pitch = Component(EpicsMotor, '8idi:m67', labels=["motor", "crl", "optics"])
    yaw = Component(EpicsMotor, '8idi:m66', labels=["motor", "crl", "optics"])


class MonochromatorTableDevice(Device):
    """
    Table TI-1 in 8-ID-I
    """
    x = Component(EpicsMotor, '8idi:TI1:x', labels=["motor", "mono", "optics", "table"])
    z = Component(EpicsMotor, '8idi:TI1:y', labels=["motor", "mono", "optics", "table"])


class MonochromatorDevice(Device):
    energy = Component(EpicsMotor, '8idimono:sm2', labels=["motor", "mono", "optics"])
    theta = Component(EpicsMotor, '8idimono:sm1', labels=["motor", "mono", "optics"])
    piezo = Component(EpicsMotor, '8idimono:m4', labels=["motor", "mono", "optics"])
    pico = Component(EpicsMotor, '8idimono:m1', labels=["motor", "mono", "optics"])
    nano = Component(EpicsMotor, '8idimono:m5', labels=["motor", "mono", "optics"])
    table = Component(MonochromatorTableDevice, labels=["mono", "optics", "table"])


class WBslitDevice(Device):  
    """
    White Beam Slit in 8-ID-A
    """
    vgap = Component(EpicsMotor, '8ida:Slit1Vsize', labels=["motor", "slit"])
    vcen = Component(EpicsMotor, '8ida:Slit1Vcenter', labels=["motor", "slit"])
    hgap = Component(EpicsMotor, '8ida:Slit1Hsize', labels=["motor", "slit"])
    hcen = Component(EpicsMotor, '8ida:Slit1Hcenter', labels=["motor", "slit"])
    zu = Component(EpicsMotor, '8ida:m11', labels=["motor", "slit"])    
    xu = Component(EpicsMotor, '8ida:m14', labels=["motor", "slit"])    
    zd = Component(EpicsMotor, '8ida:m15', labels=["motor", "slit"])
    xd = Component(EpicsMotor, '8ida:m16', labels=["motor", "slit"])


class SlitI1Device(Device):  
    """
    Slit1 in 8-ID-I
    """
    x = Component(EpicsMotor, '8idi:m18', labels=["motor", "slit"])
    vgap = Component(EpicsMotor, '8idi:Slit1Vsize', labels=["motor", "slit"])
    vcen = Component(EpicsMotor, '8idi:Slit1Vcenter', labels=["motor", "slit"])
    hgap = Component(EpicsMotor, '8idi:Slit1Hsize', labels=["motor", "slit"])
    hcen = Component(EpicsMotor, '8idi:Slit1Hcenter', labels=["motor", "slit"])


class SlitI2Device(Device):  
    """
    Slit2 in 8-ID-I
    """
    vgap = Component(EpicsMotor, '8idi:Slit2Vsize', labels=["motor", "slit"])
    vcen = Component(EpicsMotor, '8idi:Slit2Vcenter', labels=["motor", "slit"])
    hgap = Component(EpicsMotor, '8idi:Slit2Hsize', labels=["motor", "slit"])
    hcen = Component(EpicsMotor, '8idi:Slit2Hcenter', labels=["motor", "slit"])    


class SlitI3Device(Device):  
    """
    Slit3 in 8-ID-I
    """
    vgap = Component(EpicsMotor, '8idi:Slit3Vsize', labels=["motor", "slit"])
    vcen = Component(EpicsMotor, '8idi:Slit3Vcenter', labels=["motor", "slit"])
    hgap = Component(EpicsMotor, '8idi:Slit3Hsize', labels=["motor", "slit"])
    hcen = Component(EpicsMotor, '8idi:Slit3Hcenter', labels=["motor", "slit"])    


class SlitI4Device(Device):  
    """
    Slit4 in 8-ID-I
    """
    vgap = Component(EpicsMotor, '8idi:Slit4Vsize', labels=["motor", "slit"])
    vcen = Component(EpicsMotor, '8idi:Slit4Vcenter', labels=["motor", "slit"])
    hgap = Component(EpicsMotor, '8idi:Slit4Hsize', labels=["motor", "slit"])
    hcen = Component(EpicsMotor, '8idi:Slit4Hcenter', labels=["motor", "slit"])    


class SlitI5Device(Device):  
    """
    Slit5 in 8-ID-I
    """    
    x = Component(EpicsMotor, '8idi:m55', labels=["motor", "slit"])
    z = Component(EpicsMotor, '8idi:m56', labels=["motor", "slit"])
    vgap = Component(EpicsMotor, '8idi:Slit5Vsize', labels=["motor", "slit"])
    vcen = Component(EpicsMotor, '8idi:Slit5Vcenter', labels=["motor", "slit"])
    hgap = Component(EpicsMotor, '8idi:Slit5Hsize', labels=["motor", "slit"])
    hcen = Component(EpicsMotor, '8idi:Slit5Hcenter', labels=["motor", "slit"])


class SlitIpinkDevice(Device):  
    """
    Slitpink in 8-ID-I
    """    
    vgap = Component(EpicsMotor, '8idi:SlitpinkVsize', labels=["motor", "slit"])
    vcen = Component(EpicsMotor, '8idi:SlitpinkVcenter', labels=["motor", "slit"])
    hgap = Component(EpicsMotor, '8idi:SlitpinkHsize', labels=["motor", "slit"])
    hcen = Component(EpicsMotor, '8idi:SlitpinkHcenter', labels=["motor", "slit"])


class FOEpinholeDevice(Device):  
    """
    Optics Table 1 in 8-ID-A which holds the 270 um pin hole for heat load reduction
    """    
    x = Component(EpicsMotor, '8ida:TA1:x', labels=["motor", "table"]) 
    z = Component(EpicsMotor, '8ida:TA1:y', labels=["motor", "table"])
  

class FOEmirrorDevice(Device):  
    """
    Optics Table 2 in 8-ID-A which holds the First optical element Mirror
    """    
    x = Component(EpicsMotor, '8ida:TA2:x', labels=["motor", "table"])
    z = Component(EpicsMotor, '8ida:TA2:y', labels=["motor", "table"])
    theta = Component(EpicsMotor, '8ida:sm9', labels=["motor", "table"])


class BeamSplittingMonochromatorDevice(Device):  
    """
    I/E Beam-splitting Silicon monochromator in 8-ID-D
    """    
    x = Component(EpicsMotor, '8idd:m1', labels=["motor", "optics"])
    z = Component(EpicsMotor, '8idd:m2', labels=["motor", "optics"])


class TableOptics(Device):  
    """
    Optics Table 2 in 8-ID-I which holds optics and slits
    """    
    x = Component(EpicsMotor, '8idi:TI2:x', labels=["motor", "table"])
    z = Component(EpicsMotor, '8idi:TI2:y', labels=["motor", "table"])
   
 
class FlightPathTable(Device):  
    """
    Optics Table 4 in 8-ID-I
    """    
    x = Component(EpicsMotor, '8idi:TI4:x', labels=["motor", "table"])
    z = Component(EpicsMotor, '8idi:TI4:y', labels=["motor", "table"])
    zu = Component(EpicsMotor, '8idi:m30', labels=["motor", ])
    zdo = Component(EpicsMotor, '8idi:m31', labels=["motor", ])
    zdi = Component(EpicsMotor, '8idi:m32', labels=["motor", ])
    xu = Component(EpicsMotor, '8idi:m28', labels=["motor", ])
    xd = Component(EpicsMotor, '8idi:m29', labels=["motor", ])
 

class BeWindow(Device):  
    """
    Beryllium Window 8-ID-I
    """    
    x = Component(EpicsMotor, '8idi:m17', labels=["motor", "optics"])
    z = Component(EpicsMotor, '8idi:m11', labels=["motor", "optics"])

        
class ShutterStage(Device):  
    """
    Shutter Stage at 8-ID-I
    """    
    x = Component(EpicsMotor, '8idi:m1', labels=["motor", "shutter"])
    z = Component(EpicsMotor, '8idi:m2', labels=["motor", "shutter"])
    
            
class DetStageUpstream(Device):  
    """
    Upstream detector stage at 4 m (the old 'ccdx' and 'ccdz')
    """    
    x = Component(EpicsMotor, '8idi:m90', labels=["motor", "det"])
    z = Component(EpicsMotor, '8idi:m91', labels=["motor", "det"])
  

class DetStageDownstream(Device):  
    """
    Downstream detector stage at 8 m (the old 'fccdx' and 'fccdz')
    """    
    x = Component(EpicsMotor, '8idi:m25', labels=["motor", "det"])
    z = Component(EpicsMotor, '8idi:m83', labels=["motor", "det"])

    
#class SamplePiezo(Device):  
#    """
#    Piezo stage at the sample?
#    """    
#    x = Component(EpicsMotor, '8idi:m69', labels=["motor", "sample"])
#    z = Component(EpicsMotor, '8idi:m70', labels=["motor", "sample"])


class SampleStageTable(Device):
    """
    Sample stage table TI-3
    """
    x = Component(EpicsMotor, '8idi:TI3:x', labels=["motor", "table", "sample"])
    y = Component(EpicsMotor, '8idi:TI3:z', labels=["motor", "table", "sample"])
    z = Component(EpicsMotor, '8idi:TI3:y', labels=["motor", "table", "sample"])


class SampleStage(Device):
    """
    Sample stage 
    """
    x = Component(EpicsMotor, '8idi:m54', labels=["motor", "sample"])
    y = Component(EpicsMotor, '8idi:m49', labels=["motor", "sample"])
    z = Component(EpicsMotor, '8idi:m50', labels=["motor", "sample"])
    phi = Component(EpicsMotor, '8idi:m51', labels=["motor", "sample"])     # yaw
    theta = Component(EpicsMotor, '8idi:m52', labels=["motor", "sample"])   # pitch
    chi = Component(EpicsMotor, '8idi:m53', labels=["motor", "sample"])     # roll
    table = Component(SampleStageTable, labels=["table",])

    # used by the movesample plans
    nextpos = 0
    xdata = np.linspace(0, 2, 21)    # example: user will change this
    zdata = np.linspace(0, .5, 15)    # example: user will change this

    def movesample(self):
        if dm_pars.geometry_num.get() == 0: # transmission
            xn = len(self.xdata)
            zn = len(self.zdata)
            if xn > zn:
                x = self.nextpos % xn
                z = int(self.nextpos/xn) % zn
            else:
                x = int(self.nextpos/zn) % xn
                z = self.nextpos % zn
        else:    # reflection
            x = self.nextpos % len(self.xdata)
            z = self.nextpos % len(self.zdata)

        x = self.xdata[x]
        z = self.zdata[z]
        logger.info(f"Moving samx to {x}, samz to {z}")
        yield from bps.mv(
            self.x, x,
            self.z, z,
            )
        self.nextpos += 1

    def movesamx(self):
        index = self.nextpos % len(self.xdata)
        p = self.xdata[index]
        logger.info(f"Moving samx to {p}")
        yield from bps.mv(self.x, p)
        self.nextpos += 1

    def movesamz(self):
        index = self.nextpos % len(self.zdata)
        p = self.zdata[index]
        logger.info(f"Moving samz to {p}")
        yield from bps.mv(self.z, p)
        self.nextpos += 1


class LS336_LoopBase(APS_devices.ProcessController):
    """
    One control loop on the LS336 temperature controller
    
    Each control loop is a separate process controller.
    """
    signal = FormattedComponent(EpicsSignalRO, "{self.prefix}OUT{self.loop_number}:SP_RBV")
    target = FormattedComponent(EpicsSignal, "{self.prefix}OUT{self.loop_number}:SP", kind="omitted")
    units = FormattedComponent(EpicsSignalWithRBV, "{self.prefix}IN{self.loop_number}:Units", kind="omitted")

    loop_name = FormattedComponent(EpicsSignalRO, "{self.prefix}IN{self.loop_number}:Name_RBV")
    temperature = FormattedComponent(EpicsSignalRO, "{self.prefix}IN{self.loop_number}")

    control = FormattedComponent(EpicsSignalWithRBV, "{self.prefix}OUT{self.loop_number}:Cntrl")
    manual = FormattedComponent(EpicsSignalWithRBV, "{self.prefix}OUT{self.loop_number}:MOUT")
    mode = FormattedComponent(EpicsSignalWithRBV, "{self.prefix}OUT{self.loop_number}:Mode")

    def __init__(self, *args, loop_number=None, **kwargs):
        self.controller_name = f"Lakeshore 336 Controller Loop {loop_number}"
        self.loop_number = loop_number
        super().__init__(*args, **kwargs)

    @property
    def settled(self):
        """Is temperature close enough to target?"""
        diff = abs(self.temperature.get() - self.target.get())
        return diff <= self.tolerance.get()

    def get(self, *args, **kwargs):
        return self.signal.get(*args, **kwargs)

    def wait_until_settled(self, timeout=None, timeout_fail=False):
        """
        plan: wait for controller signal to reach target within tolerance
        """
        # see: https://stackoverflow.com/questions/2829329/catch-a-threads-exception-in-the-caller-thread-in-python
        t0 = time.time()
        _st = DeviceStatus(self.signal)

        if self.settled:
            # just in case signal already at target
            _st._finished(success=True)
        else:
            started = False
    
            def changing_cb(*args, **kwargs):
                if started and self.settled:
                    _st._finished(success=True)
    
            token = self.signal.subscribe(changing_cb)
            started = True
            report = 0
            while not _st.done and not self.settled:
                elapsed = time.time() - t0
                if timeout is not None and elapsed > timeout:
                    _st._finished(success=self.settled)
                    msg = f"{self.controller_name} Timeout after {elapsed:.2f}s"
                    msg += f", target {self.target.get():.2f}{self.units.get()}"
                    msg += f", now {self.signal.get():.2f}{self.units.get()}"
                    print(msg)
                    if timeout_fail:
                        raise TimeoutError(msg)
                    continue
                if elapsed >= report:
                    report += self.report_interval_s
                    msg = f"Waiting {elapsed:.1f}s"
                    msg += f" to reach {self.target.get():.2f}{self.units.get()}"
                    msg += f", now {self.temperature.get():.2f}{self.units.get()}"
                    print(msg)
                yield from bps.sleep(self.poll_s)

            self.signal.unsubscribe(token)
            _st._finished(success=self.settled)

        self.record_signal()
        elapsed = time.time() - t0
        print(f"Total time: {elapsed:.3f}s, settled:{_st.success}")


class LS336_LoopMore(LS336_LoopBase):
    """
    Additional controls for loop1 and loop2: heater and pid
    """
    # only on loops 1 & 2
    heater = FormattedComponent(EpicsSignalRO, "{self.prefix}HTR{self.loop_number}")
    heater_range = FormattedComponent(EpicsSignalWithRBV, "{self.prefix}HTR{self.loop_number}:Range")

    pid_P = FormattedComponent(EpicsSignalWithRBV, "{self.prefix}P{self.loop_number}")
    pid_I = FormattedComponent(EpicsSignalWithRBV, "{self.prefix}I{self.loop_number}")
    pid_D = FormattedComponent(EpicsSignalWithRBV, "{self.prefix}D{self.loop_number}")
    ramp_rate = FormattedComponent(EpicsSignalWithRBV, "{self.prefix}RampR{self.loop_number}")
    ramp_on = FormattedComponent(EpicsSignalWithRBV, "{self.prefix}OnRamp{self.loop_number}")


from records.asyn import AsynRecord


class LS336Device(Device):
    """
    support for Lakeshore 336 temperature controller
    """
    loop1 = FormattedComponent(LS336_LoopMore, "{self.prefix}", loop_number=1)
    loop2 = FormattedComponent(LS336_LoopMore, "{self.prefix}", loop_number=2)
    loop3 = FormattedComponent(LS336_LoopBase, "{self.prefix}", loop_number=3)
    loop4 = FormattedComponent(LS336_LoopBase, "{self.prefix}", loop_number=4)
    
    # same names as apstools.synApps._common.EpicsRecordDeviceCommonAll
    scanning_rate = Component(EpicsSignal, "read.SCAN")
    process_record = Component(EpicsSignal, "read.PROC")
    
    read_all = Component(EpicsSignal, "readAll.PROC")
    serial = Component(AsynRecord, "serial")

    @property
    def value(self):
        """designate one loop as the default signal to return"""
        return self.loop1.signal.get()


class PSS_Parameters(Device):
    a_beam_active = Component(EpicsSignalRO, "PA:08ID:A_BEAM_ACTIVE.VAL", string=True, labels=["pss",])

    d_shutter_open_chain_A = Component(EpicsSignalRO, "PA:08ID:STA_D_SDS_OPEN_PL.VAL", string=True, labels=["pss",])
    d_shutter_closed_chain_B = Component(EpicsSignalRO, "PB:08ID:STA_D_SDS_CLSD_PL", string=True, labels=["pss",])

    i_shutter_open_chain_A = Component(EpicsSignalRO, "PA:08ID:STA_F_SFS_OPEN_PL", string=True, labels=["pss",])
    i_shutter_closed_chain_B = Component(EpicsSignalRO, "PB:08ID:STA_F_SFS_CLSD_PL", string=True, labels=["pss",])
    i_station_searched_chain_A = Component(EpicsSignalRO, "PA:08ID:STA_F_SEARCHED_PL.VAL", string=True, labels=["pss",])

    @property
    def i_station_enabled(self):
        """
        look at the switches: are we allowed to operate?
    
        # Station I has a shutter to control beam entering
        # but the user may open or close that shutter at will.
        # The upstream D shutter (at exit of A station) defines 
        # whether the I station can operate,
        # so that's the component we need to make a determination
        # whether or not the I station is enabled.
        
        # I station operations are enabled if D shutter is OPEN
        """
        enabled = self.d_shutter_open_chain_A.get() == "ON"
        return enabled


class PreampUnitNumberDevice(Device):
    units = Component(EpicsSignalRO, 'sens_unit', string=True)
    number = Component(EpicsSignalRO, 'sens_num')
    
    unit_gains = {
		"mA/V": 1e-3,
		"uA/V": 1e-6,
		"nA/V": 1e-9,
		"pA/V": 1e-12,
	}

    @property
    def amp_scale(self):
        enums = self.number.enum_strs
        sensitivity_index = self.number.get()
        sensitivity = float(enums[sensitivity_index])

        units = self.units.get()
        gain = self.unit_gains[units]

        return gain * sensitivity


class PreampDevice(Device):
    pind1 = Component(PreampUnitNumberDevice, '8idi:A1')
    pind2 = Component(PreampUnitNumberDevice, '8idi:A2')
    pind3 = Component(PreampUnitNumberDevice, '8idi:A3')
    pind4 = Component(PreampUnitNumberDevice, '8idi:A4')
    pdbs = Component(PreampUnitNumberDevice, '8idi:A5')

    @property
    def gains(self):
        """
        return dictionary of Amps/V (gains) for all preamplifiers
        """
        Amps_per_Volt = {}
        for nm in self.component_names:
            amp = self.__getattribute__(nm)
            Amps_per_Volt[nm] = amp.amp_scale
        return Amps_per_Volt


class SoftGlueDevice(Device):

    start_trigger_pulses_sig = Component(EpicsSignal, '8idi:softGlueA:MUX2-1_IN0_Signal')
    reset_trigger_pulses_sig = Component(EpicsSignal, '8idi:softGlueA:OR-1_IN2_Signal')

    # sends  external pulse train signal to the trigger
    # this is a stringout record, value is a str
    send_ext_pulse_tr_sig_to_trig = Component(EpicsSignal, '8idi:softGlueB:BUFFER-1_IN_Signal')

    # sets shutter signal pulse train to single(0)/burst(1) mode
    # this is a stringout record, value is a str
    set_shtr_sig_pulse_tr_mode = Component(EpicsSignal, '8idi:softGlueC:MUX2-1_SEL_Signal')

    # sends detector signal pulse train to burst mode
    # this is a stringout record, value is a str
    send_det_sig_pulse_tr_mode = Component(EpicsSignal, '8idi:softGlueC:MUX2-2_SEL_Signal')

    #this should be 0 or 1 to select the pulse source to be manual or external user device driven respectively
    # this is a stringout record, value is a str
    select_pulse_train_source = Component(EpicsSignal, '8idi:softGlueA:MUX2-1_SEL_Signal')

    acquire_ext_trig_status = Component(EpicsSignal, '8idi:softGlueA:FI2_BI')

    def start_trigger(self):
        # from SPEC macro: Start_SoftGlue_Trigger
        if self.select_pulse_train_source.get() == '0':
            logger.info("Starting detector trigger pulses")
            yield from bps.mv(self.start_trigger_pulses_sig, "1!")
        else:
            logger.info("Waiting for ****User Trigger**** to start acquisition")

    def reset_trigger(self):
        # from SPEC macro: Reset_SoftGlue_Trigger
        logger.info("Resetting detector trigger pulses")
        yield from bps.mv(self.reset_trigger_pulses_sig, "1!")


class PSO_TaxiFly_Device(Device):
    """
    Operate the motion trajectory controls of an Aerotech Ensemble controller
    
    note: PSO means Position Synchronized Output (Aerotech's term)
    
    USAGE:
    
        # create an object
        pso1 = PSO_TaxiFly_Device("2bmb:PSOFly1:", name="pso1")
        
        # in a plan, use this
        yield from abs_set(pso1, "taxi", wait=True)
        yield from abs_set(pso1, "fly", wait=True)
    """
    slew_speed = Component(EpicsSignal, "slewSpeed.VAL")
    scan_control = Component(EpicsSignal, "scanControl.VAL", string=True)
    start_pos = Component(EpicsSignal, "startPos.VAL")
    end_pos = Component(EpicsSignal, "endPos.VAL")
    scan_delta = Component(EpicsSignal, "scanDelta.VAL")
    pso_taxi = Component(EpicsSignal, "taxi.VAL", put_complete=True)
    pso_fly = Component(EpicsSignal, "fly.VAL", put_complete=True)
    busy = Signal(value=False, name="busy")

    enabled = True  # True or False  (was `FLY_SCAN_YES_NO` in SPEC)
    
    def setup(self, start_pos, end_pos, slew_speed):
        """
        convenience plan: define the fly scan range parameters
        """
        yield from bps.mv(
            self.start_pos, start_pos,
            self.end_pos, end_pos,
            self.slew_speed, slew_speed,
        )
    
    def taxi(self):
        """
        request move to taxi position, interactive use

        Note: This method is NOT a bluesky plan.
        
        Since ``pso_taxi`` has the ``put_complete=True`` attribute,
        this will block until the move is complete.
        
        (note: ``2bmb:PSOFly1:taxi.RTYP`` is a ``busy`` record.)
        """
        logger.debug("starting TAXI to position")
        self.pso_taxi.put("Taxi")
    
    def fly(self):
        """
        request fly scan to start, interactive use

        Note: This method is NOT a bluesky plan.
        
        Since ``pso_fly`` has the ``put_complete=True`` attribute,
        this will block until the move is complete.
        """
        logger.debug("starting FLY")
        self.pso_fly.put("Fly")

    def set(self, value):       # interface for BlueSky plans
        """value is either Taxi or Fly"""
        # """value is either Taxi, Fly, or Return"""
        allowed = "Taxi Fly".split()
        if str(value).lower() not in list(map(str.lower, allowed)):
            msg = "value should be one of: " + " | ".join(allowed)
            msg + " received " + str(value)
            raise ValueError(msg)

        if self.busy.get():
            raise RuntimeError("PSO device is operating")

        status = DeviceStatus(self)
        
        def action():
            """the real action of ``set()`` is here"""
            if str(value).lower() == "taxi":
                self.taxi()
            elif str(value).lower() == "fly":
                self.fly()
            # elif str(value).lower() == "return":
            #     self.motor.move(self.return_position)

        def run_and_wait():
            """handle the ``action()`` in a thread"""
            self.busy.put(True)
            action()
            self.busy.put(False)
            status._finished(success=True)
        
        threading.Thread(target=run_and_wait, daemon=True).start()
        return status


class DM_DeviceMixinBase(Device):
    """
    methods and attributes used by the APS Data Management workflow support
    """

    def staging_setup_DM(self, *args, **kwargs):
        """
        setup the device's stage_sigs for acquisition with the DM workflow

        Implement this method in _any_ Device that requires custom
        setup for the DM workflow.

        Not a bluesky "plan" (no "yield from")
        """
        # logger.debug(f"staging_setup_DM({args})")
        raise NotImplementedError("must override in subclass")


class DM_DeviceMixinScaler(DM_DeviceMixinBase):
    """for use with ScalerCH and the DM workflow"""


class DM_DeviceMixinAreaDetector(DM_DeviceMixinBase):
    """for use with area detector and the DM workflow"""

    qmap_file = ""              # TODO: documentation?
    detector_number = None      # 8-ID-I numbering of this detector
    
    @property
    def plugin_file_name(self):
        """
        return the (base, no path) file name the plugin wrote
        
        Implement for the DM workflow.

        Not a bluesky "plan" (no "yield from")
        """
        # logger.debug(f"plugin_file_name({args})")
        raise NotImplementedError("must override in subclass")

    def xpcs_loop(self, *args, **kwargs):
        """
        Combination of `xpcs_pre_start_LAMBDA` and `user_xpcs_loop_LAMBDA`

        see: https://github.com/aps-8id-trr/ipython-8idiuser/issues/107
        """
        # logger.debug(f"xpcs_loop({args})")
        raise NotImplementedError("must override in subclass")