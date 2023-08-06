import os
import sys


async def load_uname(hub):
    """
    Verify that idem-solaris is running on SunOS
    """
    (
        hub.corn.CORN.kernel,
        hub.corn.CORN.nodename,
        hub.corn.CORN.kernelrelease,
        hub.corn.CORN.kernelversion,
        hub.corn.CORN.osarch,
    ) = os.uname()

    assert (
        hub.corn.CORN.kernel == "SunOS"
    ), "idem-solaris is only intended for SunOs systems"

    # Determine if host is SmartOS (Illumos) or not
    hub.corn.CORN.smartos = sys.platform.startswith(
        "sunos"
    ) and hub.corn.CORN.kernelversion.startswith("joyent_")

    # Hard coded grains for SunOs go here:
