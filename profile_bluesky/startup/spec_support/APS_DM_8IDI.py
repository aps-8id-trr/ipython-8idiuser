
"""
support for the APS Data Management tools

Starting in January 2018, we are trying to move towards SDM Group product as part of DM or Data
Management developed by Sinisa Veseli. This primarily has tools to move data to the storage server with
cataloging tools. Additionally, this has workflow processing tools which are all done in python along with
shell scripts. With Faisal's new xpcs analysis toolkit, we will be using Sun Grid Engine (SGE) for job
submission. So it is time to move away from the Active MQ pipeline with the actors, etc. 

Sinisa has set up workflows: one for data transfer using GridFTP and the other to do full analysis. He has
also developed SGE submission and monitoring which is very helpful. The downside as of now is that there
is no GUI that shows the job status which was a plus with the old pipeline. A GUI will be developed in the
near future.

These workflows are stored in ~8idiuser/DM_Workflows/ and in https://subversion.xray.aps.anl.gov/xpcs/DM_Workflows/
"""

import datetime
import h5py
import logging
import math
import os
import re
import subprocess
import sys
import threading
import time

from . import detector_parameters


logger = logging.getLogger(f"main.{__name__}")


def unix(command, raises=True):
    """
    run a UNIX command, returns (stdout, stderr)

    from apstools.utils.unix()

    PARAMETERS
    
    command: str
        UNIX command to be executed
    raises: bool
        If `True`, will raise exceptions as needed,
        default: `True`
    """
    if sys.platform not in ("linux", "linux2"):
        emsg = f"Cannot call unix() when OS={sys.platform}"
        raise RuntimeError(emsg)

    stdout, stderr = "", ""
    with subprocess.Popen(
        command, 
        shell=True,
        stdin = subprocess.PIPE,
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE,
        ) as process:

        stdout, stderr = process.communicate()

        if len(stderr) > 0:
            emsg = f"unix({command}) returned error:\n{stderr}"
            logger.error(emsg)
            if raises:
                raise RuntimeError(emsg)

    return stdout, stderr


def run_in_thread(func):
    """
    (decorator) run ``func`` in thread

    from apstools.utils.run_in_thread()
    
    USAGE::

       @run_in_thread
       def progress_reporting():
           logger.debug("progress_reporting is starting")
           # ...
       
       #...
       progress_reporting()   # runs in separate thread
       #...

    """
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=func, args=args, kwargs=kwargs)
        thread.start()
        return thread
    return wrapper


class DM_Workflow:
    """
    support for the APS Data Management tools
        
    PARAMETERS
    
    registers : ophyd.Device or spec_DM_support.DataManagementMetadata
        Instance of class, connected to metadata register PVs
    
    transfer : str, optional
        Data Management Workflow transfer key (DM_WORKFLOW_DATA_TRANSFER)
    
    analysis : str, optional
        Data Management Workflow analysis key (DM_WORKFLOW_DATA_ANALYSIS)
    
    qmap_path : str, optional
        qmap file directory (QMAP_FOLDER_PATH)
    
    xpcs_qmap_file : str, optional
        XPCS qmap file name (XPCS_QMAP_FILENAME)

    ======================  ===========================================
    method                  docstring
    ======================  ===========================================
    get_workflow_filename   decide absolute file name for the APS data management workflow
    start_workflow          commence the APS data management workflow
    set_xpcs_qmap_file      (re)define the name of HDF5 workflow file
    create_hdf5_file        Reads camera data from EPICS PVs and writes to an hdf5 file
    DataTransfer            initiate data transfer
    DataAnalysis            initiate data analysis
    ListJobs                list current jobs in the workflow
    ======================  ===========================================
    """

    def __init__(self, 
                 registers,
                 aps_cycle,
                 xpcs_qmap_file,
                 transfer="xpcs8-01-Lambda",
                 analysis="xpcs8-02-Lambda",
                 ):
        logger.info(f"setting up DM_Workflow() for APS operating cycle {aps_cycle}")
        self.registers = registers
        self.detectors = detector_parameters.PythonDict()

        self.transfer = transfer      # was DM_WORKFLOW_DATA_TRANSFER
        self.analysis = analysis      # was DM_WORKFLOW_DATA_ANALYSIS
        # self.transfer = "xpcs8-01-nos8iddata"
        # self.analysis = "xpcs8-02-nos8iddata"
        self.TRANSFER_COMMAND = ""
        self.ANALYSIS_COMMAND = ""
        
        self.QMAP_FOLDER_PATH = f"/home/8-id-i/partitionMapLibrary/{aps_cycle}"
        self.set_xpcs_qmap_file(xpcs_qmap_file)

        self.hdf_workflow_file = None

    def cleanupFilename(self, text):
        """
        convert text so it can be used as a file name
        Given some input text string, return a clean version
        remove troublesome characters, perhaps other cleanup as well.
        This is best done with regular expression pattern matching.

        This ONLY cleans the base name.

        EXAMPLE:

        This gets cleaned up::

            cleanupFilename("/good/path/to/bad file &^$*&^(&) name.txt")

        No changes with this::

            cleanupFilename("/ bad $$ &^%%$ path with/good_file_name.txt")

        """
        path, base = os.path.split(text)
        base, ext = os.path.splitext(base)

        pattern = "[a-zA-Z0-9_]"

        def mapper(c):
            if re.match(pattern, c) is not None:
                return c
            return "_"

        base = "".join([mapper(c) for c in base])
        result = os.path.join(path, base+ext)
        if result != text:
            msg = f"cleaned file name, was: '{text}'   now: '{result}'"
            logger.info(msg)
        return result

    def get_workflow_filename(self):
        """
        decide absolute file name for the APS data management workflow
        """
        registers = self.registers
        path = registers.root_folder.get()
        if path.startswith("/data"):
            path = os.path.join("/", "home", "8-id-i", *path.split("/")[2:])
        data_folder = self.cleanupFilename(registers.data_folder.get().strip('/'))
        path = os.path.join(path, data_folder, registers.data_subfolder.get())
        fname = (
            f"{data_folder}"
            f"_{registers.data_begin.get():04.0f}"
            f"-{registers.data_end.get():04.0f}"
        )
        fullname = os.path.join(path, f"{fname}.hdf")
        suffix = 0
        while os.path.exists(fullname):
            suffix += 1
            fullname = os.path.join(path, f"{fname}__{suffix:03d}.hdf")
        if suffix > 0:
            logger.info(f"using modified file name: {fullname}")
        return fullname

    def start_workflow(self, analysis=True):
        """
        commence the APS data management workflow
        
        PARAMETERS
        
        hdf_workflow_file : str
            name of the HDF5 workflow file to be written
        
        analysis : bool
            If True (default): use DataAnalysis workflow.
            If False: use DataTransfer workflow.
        """
        analysis = analysis in (1, 1.0, True)
        wf_name = {True: "analysis", False: "transfer"}[analysis]
        logger.info(f"starting start_workflow(): workflow:{wf_name}")
        
        @run_in_thread
        def kickoff_DM_workflow():
            msg = f"DM workflow starting: workflow:{wf_name}  file:{self.hdf_workflow_file}"
            logger.info(f"{msg}")
            t1 = time.time()
            try:
                func = {
                    True: self.DataAnalysis, 
                    False: self.DataTransfer
                }[analysis]
                out_err = func(self.hdf_workflow_file)
                out = out_err[0].decode().strip()
                err = out_err[1].decode().strip()
            except Exception as exc:
                logger.warning(f"Exception {exc}")
            dt1 = time.time() - t1
            logger.info(f"{out}")
            # TODO: this is the place to get the job's UID
            # out="id=a5b0f25e-b8e1-4fa2-9c22-580379d47d0c owner=8idiuser status=pending startTime=1571151502.86 startTimestamp=2019/10/15 09:58:22 CDT"
            # if len(out) > 20:
            #     uid = out.split()[0].split("=")[-1]
            logger.info(f"DM workflow kickoff done: {dt1:.3f}s")
            if len(err) > 0:
                logger.info(f"{err}")
        
        logger.info("starting start_workflow()")
        self.hdf_workflow_file = self.get_workflow_filename()
        logger.info(f"creating hdf_workflow_file = {self.hdf_workflow_file}")
        self.create_hdf5_file(self.hdf_workflow_file)
        logger.info(f"hdf_workflow_file exists: {os.path.exists(self.hdf_workflow_file)}")

        logger.debug("calling kickoff_DM_workflow()")
        t0 = time.time()
        kickoff_DM_workflow()
        dt = time.time() - t0
        logger.debug(f"after kickoff_DM_workflow(): {dt:.3f}s")

    def set_xpcs_qmap_file(self, xpcs_qmap_file):
        """
        (re)define the name of HDF5 workflow file
        
        PARAMETERS
        
        xpcs_qmap_file : str
            name of the HDF5 workflow file to be written
        """
        ext = ".h5"
        if not xpcs_qmap_file.endswith(ext):
            xpcs_qmap_file = os.path.splitext(xpcs_qmap_file)[0] + ext
        self.XPCS_QMAP_FILENAME = xpcs_qmap_file

    def create_hdf5_file(self, filename, **kwargs):
        """
        write metadata from EPICS PVs to new HDF5 file
        
        PARAMETERS
        
        filename : str
            name of the HDF5 file to be written
        """
        registers = self.registers

        # Gets Python Dict stored in other file
        masterDict = self.detectors.getMasterDict()

        logger.info(f"creating HDF5 file {filename}")
        
        # any exception here will be handled by caller
        with h5py.File(filename, "w-") as f:
            # get a version number so we can make changes without breaking client code
            f.create_dataset("/hdf_metadata_version",
                data=[[registers.hdf_metadata_version.get()]]) #same as batchinfo_ver for now
            ##version 15 (May 2019) is start of burst mode support (rigaku) 

            #######/measurement/instrument/acquisition
            #######some new acq fields to replace batchinfo
            f.create_dataset("/measurement/instrument/acquisition/dark_begin",
                data=[[registers.dark_begin.get()]],
                dtype='uint64'
                )

            f.create_dataset("/measurement/instrument/acquisition/dark_end",
                data=[[registers.dark_end.get()]],
                dtype='uint64'
                )

            f.create_dataset("/measurement/instrument/acquisition/data_begin",
                data=[[registers.data_begin.get()]],
                dtype='uint64'
                )

            f.create_dataset("/measurement/instrument/acquisition/data_end",
                data=[[registers.data_end.get()]],
                dtype='uint64'
                )

            f.create_dataset("/measurement/instrument/acquisition/specscan_dark_number",
                data=[[registers.specscan_dark_number.get()]],
                dtype='uint64'
                )

            f.create_dataset("/measurement/instrument/acquisition/specscan_data_number",
                data=[[registers.specscan_data_number.get()]],
                dtype='uint64'
                )

            f.create_dataset("/measurement/instrument/acquisition/attenuation",
                data=[[registers.attenuation.get()]])
            
            f.create_dataset("/measurement/instrument/acquisition/beam_size_H",
                data=[[registers.beam_size_H.get()]])
            
            f.create_dataset("/measurement/instrument/acquisition/beam_size_V",
                data=[[registers.beam_size_V.get()]])

            f["/measurement/instrument/acquisition/specfile"] = registers.specfile.get()

            # registers.root_folder: '/home/8-id-i/2019-2/jemian_201908/A024/'
            # registers.data_subfolder: 'A186_DOHE04_Yb010_att0_Uq0_00150'
            # root_folder: '/home/8-id-i/2019-2/jemian_201908/A024/A186_DOHE04_Yb010_att0_Uq0_00150/'
            root_folder = os.path.join(
                registers.root_folder.get(),
                registers.data_subfolder.get()
            ).rstrip("/") + "/"  # ensure one and only one trailing `/`
            f["/measurement/instrument/acquisition/root_folder"] = root_folder

            # In [1]: registers.user_data_folder.get()
            # Out[1]: '/home/8-id-i/2019-2/jemian_201908/A024'
            # pick "jemian_201908" part
            parent_folder = registers.user_data_folder.get()
            if parent_folder.find("/") > -1:
                parent_folder = parent_folder.split("/")[-2]
            f["/measurement/instrument/acquisition/parent_folder"] = parent_folder

            f["/measurement/instrument/acquisition/data_folder"] = registers.data_folder.get()
            f["/measurement/instrument/acquisition/datafilename"] = registers.datafilename.get()

            f.create_dataset("/measurement/instrument/acquisition/beam_center_x",
                data=[[registers.beam_center_x.get()]])

            f.create_dataset("/measurement/instrument/acquisition/beam_center_y",
                data=[[registers.beam_center_y.get()]])

            f.create_dataset("/measurement/instrument/acquisition/stage_zero_x",
                data=[[registers.stage_zero_x.get()]])

            f.create_dataset("/measurement/instrument/acquisition/stage_zero_z",
                data=[[registers.stage_zero_z.get()]])

            f.create_dataset("/measurement/instrument/acquisition/stage_x",
                data=[[registers.stage_x.get()]])

            f.create_dataset("/measurement/instrument/acquisition/stage_z",
                data=[[registers.stage_z.get()]])

            v = {True: "ENABLED", 
                 False: "DISABLED"}[registers.compression.get() == 1]
            f["/measurement/instrument/acquisition/compression"] = v

            if registers.geometry_num.get() == 1: ##reflection geometry
                f.create_dataset("/measurement/instrument/acquisition/xspec",
                    data=[[float(registers.xspec.get())]],
                    dtype='float64')

                f.create_dataset("/measurement/instrument/acquisition/zspec",
                    data=[[float(registers.zspec.get())]],
                    dtype='float64')

                f.create_dataset("/measurement/instrument/acquisition/ccdxspec",
                    data=[[float(registers.ccdxspec.get())]],
                    dtype='float64')

                f.create_dataset("/measurement/instrument/acquisition/ccdzspec",
                    data=[[float(registers.ccdzspec.get())]],
                    dtype='float64')

                f.create_dataset("/measurement/instrument/acquisition/angle",
                    data=[[float(registers.angle.get())]],
                    dtype='float64')

            elif registers.geometry_num.get() == 0: ##transmission geometry
                f["/measurement/instrument/acquisition/xspec"] = [[float(-1)]]
                f["/measurement/instrument/acquisition/zspec"] = [[float(-1)]]
                f["/measurement/instrument/acquisition/ccdxspec"] = [[float(-1)]]
                f["/measurement/instrument/acquisition/ccdzspec"] = [[float(-1)]]
                f["/measurement/instrument/acquisition/angle"] = [[float(-1)]]

            #/measurement/instrument/source_begin
            f.create_dataset("/measurement/instrument/source_begin/beam_intensity_incident",
                data=[[registers.source_begin_beam_intensity_incident.get()]])

            f.create_dataset("/measurement/instrument/source_begin/beam_intensity_transmitted",
                data=[[registers.source_begin_beam_intensity_transmitted.get()]])

            f.create_dataset("/measurement/instrument/source_begin/current",
                data=[[registers.source_begin_current.get()]])
        
            f.create_dataset("/measurement/instrument/source_begin/energy",
			     data=[[registers.source_begin_energy.get()]])

            f["/measurement/instrument/source_begin/datetime"] = registers.source_begin_datetime.get()

            #/measurement/instrument/source_end (added in January 2019)
            f.create_dataset("/measurement/instrument/source_end/current",
                data=[[registers.source_end_current.get()]])

            f["/measurement/instrument/source_end/datetime"] = registers.source_end_datetime.get()

            ########################################################################################
            #/measurement/instrument/sample
            f.create_dataset("/measurement/sample/thickness", data=[[1.0]])
            
            f.create_dataset("/measurement/sample/temperature_A",
                data=[[registers.temperature_A.get()]])

            f.create_dataset("/measurement/sample/temperature_B",
                data=[[registers.temperature_B.get()]])

            f.create_dataset("/measurement/sample/temperature_A_set",
                data=[[registers.temperature_A_set.get()]])
            # data=[[registers.pid1.get()]])

            f.create_dataset("/measurement/sample/temperature_B_set",
                data=[[registers.temperature_B_set.get() ]])

            f.create_dataset(
                "/measurement/sample/translation",
                data=[
                    [
                        registers.translation_x.get(),
                        registers.translation_y.get(),
                        registers.translation_z.get(),
                        ]
                    ]
                )
            
            ##new dataset added on Oct 15,2018 (2018-3) to additionally add table params
            f.create_dataset(
                "/measurement/sample/translation_table",
                data=[
                    [
                        registers.translation_table_x.get(),
                        registers.translation_table_y.get(),
                        registers.translation_table_z.get(),
                         ]
                    ]
                )

            f.create_dataset(
                "/measurement/sample/orientation",
                data=[
                    [
                        registers.sample_pitch.get(),
                        registers.sample_roll.get(),
                        registers.sample_yaw.get()
                        ]
                    ]
                )

            #######/measurement/instrument/detector#########################
            detector_specs = masterDict[registers.detNum.get()]

            f["/measurement/instrument/detector/manufacturer"] = detector_specs["manufacturer"]

            ##f["/measurement/instrument/detector/model"] = detector_specs.get("model", "UNKNOWN")
    
            ##f["/measurement/instrument/detector/serial_number"] = detector_specs.get("serial_number", "UNKNOWN")

            f.create_dataset("/measurement/instrument/detector/bit_depth",
                data=[[math.ceil(math.log(detector_specs["saturation"],2))]],
                dtype='uint32')

            f.create_dataset("/measurement/instrument/detector/x_pixel_size",
                data=[[detector_specs["dpix"]]])

            f.create_dataset("/measurement/instrument/detector/y_pixel_size",
                data=[[detector_specs["dpix"]]])

            f.create_dataset("/measurement/instrument/detector/x_dimension",
                data=[[int(detector_specs["ccdHardwareColSize"])]],
                dtype='uint32')

            f.create_dataset("/measurement/instrument/detector/y_dimension",
                data=[[int(detector_specs["ccdHardwareRowSize"])]],
                dtype='uint32')

            f.create_dataset("/measurement/instrument/detector/x_binning",
                data=[[1]],
                dtype='uint32')

            f.create_dataset("/measurement/instrument/detector/y_binning",
                data=[[1]],
                dtype='uint32')

            f.create_dataset("/measurement/instrument/detector/exposure_time",
                data=[[registers.exposure_time.get()]])

            f.create_dataset("/measurement/instrument/detector/exposure_period",
                data=[[registers.exposure_period.get()]])

            if registers.burst_mode_state.get() == 1:
                f.create_dataset("/measurement/instrument/detector/burst/number_of_bursts",
                    data=[[registers.number_of_bursts.get()]], dtype='uint32')

                f.create_dataset("/measurement/instrument/detector/burst/first_usable_burst",
                    data=[[registers.first_usable_burst.get()]], dtype='uint32')

                f.create_dataset("/measurement/instrument/detector/burst/last_usable_burst",
                    data=[[registers.last_usable_burst.get()]], dtype='uint32')
            else:
                f.create_dataset("/measurement/instrument/detector/burst/number_of_bursts",
                    data=[[0]], dtype='uint32')

                f.create_dataset("/measurement/instrument/detector/burst/first_usable_burst",
                    data=[[0]], dtype='uint32')
            
                f.create_dataset("/measurement/instrument/detector/burst/last_usable_burst",
                    data=[[0]], dtype='uint32')

            f.create_dataset("/measurement/instrument/detector/distance",
                data=[[registers.detector_distance.get()]])


            choices = {True: "ENABLED", False: "DISABLED"}
            v = choices[detector_specs["flatfield"] == 1]
            f["/measurement/instrument/detector/flatfield_enabled"] = v

            # same choices
            v = choices[detector_specs["blemish"] == 1]
            f["/measurement/instrument/detector/blemish_enabled"] = v

            f.create_dataset("/measurement/instrument/detector/efficiency",
                data=[[detector_specs["efficiency"]]])

            f.create_dataset("/measurement/instrument/detector/adu_per_photon",
                data=[[detector_specs["adupphot"]]])

            if detector_specs["lld"] < 0:
                v = abs(detector_specs["lld"])
            else:
                v = 0
            f.create_dataset("/measurement/instrument/detector/lld", 
                             data=[[float(v)]], 
                             dtype='float64')

            if detector_specs["lld"] > 0:
                v = float(detector_specs["lld"])
            else:
                v = 0.0
            f.create_dataset("/measurement/instrument/detector/sigma", data=[[v]], dtype='float64')

            f.create_dataset("/measurement/instrument/detector/gain", data=[[1]], dtype='uint32')

            choices = {0: "TRANSMISSION", 1: "REFLECTION"}
            v = choices.get(registers.geometry_num.get(), "UNKNOWN")
            f["/measurement/instrument/detector/geometry"] = v

            choices = {True: "ENABLED", False: "DISABLED"}
            v = choices[registers.kinetics_state.get() == 1]
            f["/measurement/instrument/detector/kinetics_enabled"] = v

            v = choices[registers.burst_mode_state.get() == 1]
            f["/measurement/instrument/detector/burst_enabled"] = v

            #######/measurement/instrument/detector/kinetics/######
            if registers.kinetics_state.get() == 1:
                f.create_dataset("/measurement/instrument/detector/kinetics/first_usable_window", 
                    data=[[2]], dtype='uint32')

                v = int(registers.kinetics_top.get()/registers.kinetics_window_size.get())-1
                f.create_dataset("/measurement/instrument/detector/kinetics/last_usable_window", 
                    data=[[v]], dtype='uint32')

                f.create_dataset("/measurement/instrument/detector/kinetics/top", 
                    data=[[registers.kinetics_top.get()]], dtype='uint32')

                f.create_dataset("/measurement/instrument/detector/kinetics/window_size", 
                    data=[[registers.kinetics_window_size.get()]], dtype='uint32')
            else :
                f.create_dataset("/measurement/instrument/detector/kinetics/first_usable_window", 
                    data=[[0]], dtype='uint32')

                f.create_dataset("/measurement/instrument/detector/kinetics/last_usable_window", 
                    data=[[0]], dtype='uint32')

                f.create_dataset("/measurement/instrument/detector/kinetics/top", 
                    data=[[0]], dtype='uint32')

                f.create_dataset("/measurement/instrument/detector/kinetics/window_size", 
                    data=[[0]], dtype='uint32')

            #######/measurement/instrument/detector/roi/######
            f.create_dataset("/measurement/instrument/detector/roi/x1", 
                data=[[registers.roi_x1.get()]], dtype='uint32')

            f.create_dataset("/measurement/instrument/detector/roi/y1", 
                data=[[registers.roi_y1.get()]], dtype='uint32')

            f.create_dataset("/measurement/instrument/detector/roi/x2", 
                data=[[registers.roi_x2.get()]], dtype='uint32')

            f.create_dataset("/measurement/instrument/detector/roi/y2", 
                data=[[registers.roi_y2.get()]], dtype='uint32')

        #####################################################################################
        # Close file closes automatically due to the "with" opener

    def DataTransfer(self, hdf_with_fullpath):
        """
        initiate data transfer
        """
        cmd = (
            "source /home/dm/etc/dm.setup.sh; "
            "dm-start-processing-job"
            f" --workflow-name={self.transfer}"
            f" filePath:{hdf_with_fullpath}"
            )
        self.TRANSFER_COMMAND = cmd;
        logger.info(
            "DM Workflow call is made for DATA transfer: "
            f"{hdf_with_fullpath}"
            f"  ----{datetime.datetime.now()}"
            )
        return unix(cmd)

    def DataAnalysis(self, 
                     hdf_with_fullpath, 
                     qmapfile_with_fullpath=None, 
                     xpcs_group_name=None):
        """
        initiate data analysis
        
        SPEC note: hdf_with_fullpath : usually saved in global HDF5_METADATA_FILE 
        """
        logger.info(f"self.QMAP_FOLDER_PATH={self.QMAP_FOLDER_PATH}")
        logger.info(f"self.XPCS_QMAP_FILENAME={self.XPCS_QMAP_FILENAME}")

        try:
            default = os.path.join(self.QMAP_FOLDER_PATH, self.XPCS_QMAP_FILENAME)
        except Exception as exc:
            logger.warning(f"{exc}")
            default = "/xpcs"
        try:
            qmapfile_with_fullpath = qmapfile_with_fullpath or default
            xpcs_group_name = xpcs_group_name or "/xpcs"
        except Exception as exc:
            logger.warning(
                f"{exc}"
                f"default={default}"
                f"qmapfile_with_fullpath]{qmapfile_with_fullpath}"
                f"xpcs_group_name={xpcs_group_name}"
                )

        cmd = (
            "source /home/dm/etc/dm.setup.sh; "
            "dm-start-processing-job"
            f" --workflow-name={self.analysis}"
            f" filePath:{hdf_with_fullpath}"
            f" qmapFile:{qmapfile_with_fullpath}"
            f" xpcsGroupName:{xpcs_group_name}"
            )
        self.ANALYSIS_COMMAND = cmd;

        logger.info(
            f"DM Workflow call is made for XPCS Analysis: {hdf_with_fullpath}"
            f",  {qmapfile_with_fullpath}"
            f"  ----{datetime.datetime.now()}"
            )
        return unix(cmd)

    def ListJobs(self):
        """
        list current jobs in the workflow
        """
        command = (
            "source /home/dm/etc/dm.setup.sh; "
            "dm-list-processing-jobs"
            " --display-keys=startTime,endTime,sgeJobName,status,stage,runTime,id"
            " | sort -r"
            " |head -n 10"
            )
        out, err = unix(command);
        logger.info("*"*30)
        logger.info(out)
        logger.info("*"*30)
