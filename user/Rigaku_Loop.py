
"""
test that we can run user ops continuously - use Rigaku UFXC detector
"""

__all__ = """
    lambda_test
""".strip()

from instrument.session_logs import logger
logger.info(__file__)

from bluesky import plan_stubs as bps
import datetime
from instrument.devices import detu, dm_pars, rigaku
from instrument.framework import bec
from instrument.plans import AD_Acquire, movesample
import subprocess 


def rigaku_test(num_iter=2, 
                acquire_time=19.586e-6,   # cannot be changed
                acquire_period=20.114e-6, # cannot be changed
                num_images=100000,        # cannot be changed
                sample_name="test", 
                sample_prefix="A", 
                sample_suffix="Rq0", 
                analysis_true_false=True):
    """
    test XPCS acquisition with the Rigaku detector

    keep same arguments as similar Lambda test
    """

    bec.disable_plots()
    bec.disable_table()
    bec.disable_baseline()

    # increment the run number
    yield from bps.mvr(dm_pars.ARun_number, 1)

    # these numbers are not changeable for the Rigaku detector
    acquire_time = 19.586e-6
    acquire_period = acquire_time + 0.528e-6
    num_images = 100000

    for i in range(num_iter):
        if dm_pars.stop_before_next_scan.get() != 0:
            logger.info("received signal to STOP before next scan")
            yield from bps.mv(dm_pars.stop_before_next_scan, 0)
            break

        file_name = f"{sample_prefix}{dm_pars.ARun_number.get():03.0f}_{sample_name}_{sample_suffix}_{i+1:05.0f}"

        rigaku.qmap_file='qzhang202002b_Rq0_Log_S270_D27.h5'

        # yield from bps.mv(
        #     detu.x, 213.9,
        #     detu.z, 36.8)

        yield from AD_Acquire(rigaku, 
            acquire_time=acquire_time, acquire_period=acquire_period, 
            num_images=num_images, file_name=file_name,
            submit_xpcs_job=analysis_true_false,
            atten=None, path='/home/8-id-i/2020-1/qzhang202002b/',
            md={"sample_name": sample_name})
        logger.info("-"*20 + " end of acquire")

    bec.enable_baseline()
    bec.enable_table()
    bec.enable_plots()