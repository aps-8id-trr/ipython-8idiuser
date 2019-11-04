logger.info(__file__)

"""local, custom Device definitions"""


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
        return self.loop1.signal.value


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
        enabled = self.d_shutter_open_chain_A.value == "ON"
        return enabled
