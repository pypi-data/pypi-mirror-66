import aiofiles
import logging
import os
import re
import shutil
from typing import Tuple

log = logging.getLogger(__name__)

_OS_FAMILY_MAP = {
    "Solaris": "Solaris",
    "SmartOS": "Solaris",
    "OmniOS": "Solaris",
    "OpenIndiana Development": "Solaris",
    "OpenIndiana": "Solaris",
    "OpenSolaris Development": "Solaris",
    "OpenSolaris": "Solaris",
    "Oracle Solaris": "Solaris",
}


async def load_osbuild(hub):
    hub.corn.CORN.osbuild = "unknown"

    pkg = shutil.which("pkg") or "/usr/bin/pkg"
    if os.path.exists(pkg):
        ret = await hub.exec.cmd.run([pkg, "info", "kernel"])
        hub.corn.CORN.osbuild = ret.stdout.strip().split("FMRI")[-1].split(":")[-1]


def _load_oscodename(hub, osname: str, osrelease: float) -> str:
    if ("sunos" in osname and osrelease <= 4.1) or (
        "solaris" in osname and osrelease <= 1.1
    ):
        return "Valkyrie"
    elif ("sunos" in osname and osrelease <= 5) or (
        "solaris" in osname and osrelease <= 2
    ):
        return "Jupiter"
    elif "solaris" in osname:
        if osrelease < 2.5:
            return "Starburst"
        elif osrelease <= 2.6:
            return "Wave3"
        elif osrelease == 7:
            return "StoreEdge N8200"
        elif "64" in hub.corn.CORN.get("osarch", ""):
            # For the full x86_64 version of Solaris
            return "Wyoming"
        else:
            # For the current release of Solaris
            return "Nevada"
    else:
        return "unknown"
    # Chrysalis Client if Solaris intel-based NC


async def load_manufacturer(hub):
    hub.corn.CORN.osmanufacturer = "unknown"
    prtconf = shutil.which("prtconf") or "/usr/sbin/prtconf"
    if os.path.exists(prtconf):
        ret = await hub.exec.cmd.run(prtconf)
        for line in ret.stdout.splitlines():
            if "System Configuration" in line:
                # remove the system configuration line and os arch
                hub.corn.CORN.osmanufacturer = " ".join(line.split()[2:-1])
                break


async def _load_release(hub) -> Tuple[str]:
    release_file = "/etc/release"
    if os.path.isfile(release_file):
        async with aiofiles.open(release_file, "r") as fp_:
            rel_data = await fp_.read()
            try:
                release_re = re.compile(
                    r"((?:(?:Open|Oracle )?Solaris|OpenIndiana|OmniOS)\s*(?:Development)?)"
                    r"\s*(\d+\.?\d*|v\d+)\s?[A-Z]*\s?(r\d+|\d+\/\d+|oi_\S+|snv_\S+)?"
                )
                return release_re.search(rel_data).groups()
            except AttributeError:
                pass


async def load_osinfo(hub):
    # Collect some preliminary information
    (osname, osmajorrelease, osminorrelease) = await _load_release(hub) or [
        "Solaris",
        "0",
        "0",
    ]

    # Load os
    hub.corn.CORN.os = "SmartOS" if hub.corn.CORN.smartos else osname.strip()
    hub.corn.CORN.os_family = _OS_FAMILY_MAP.get(hub.corn.CORN.os, hub.corn.CORN.os)

    # Sanitize the osrelease information
    if hub.corn.CORN.smartos:
        # See https://github.com/joyent/smartos-live/issues/224
        osrelease_stamp = hub.corn.CORN.kernelversion[
            hub.corn.CORN.kernelversion.index("_") + 1 :
        ]
        hub.corn.CORN.osrelease = ".".join(
            (x or "0")
            for x in (
                osrelease_stamp.split("T")[0][0:4],
                osrelease_stamp.split("T")[0][4:6],
                osrelease_stamp.split("T")[0][6:8],
            )
        )
    elif (
        hub.corn.CORN.os == "Oracle Solaris"
        and hub.corn.CORN.kernelversion.startswith(osmajorrelease)
    ):
        # Oracla Solars 11 and up have minor version in kernelversion
        hub.corn.CORN.osrelease = hub.corn.CORN.kernelversion[
            : hub.corn.CORN.kernelversion.find(".", 5)
        ]
    elif hub.corn.CORN.os == "OmniOS":
        hub.corn.CORN.osrelease = f"{osmajorrelease[1:] or 0}.{osminorrelease[1:] or 0}"
    else:
        hub.corn.CORN.osrelease = ""

    # Load release info
    hub.corn.CORN.osrelease_info = [
        int(x) if x.isdigit() else x or 0 for x in hub.corn.CORN.osrelease.split(".")
    ]
    assert len(hub.corn.CORN.osrelease_info)
    hub.corn.CORN.osmajorrelease = int(hub.corn.CORN.osrelease_info[0])
    hub.corn.CORN.osrelease = ".".join(
        str(x or 0) for x in hub.corn.CORN.osrelease_info
    )

    # Load other name info
    if len(hub.corn.CORN.osrelease_info) > 1:
        hub.corn.CORN.oscodename = _load_oscodename(
            hub,
            osname=hub.corn.CORN.os.lower(),
            osrelease=hub.corn.CORN.osrelease_info[0]
            + (hub.corn.CORN.osrelease_info[1] / 10),
        )
    else:
        hub.corn.CORN.oscodename = "unknown"

    if hub.corn.CORN.osmajorrelease:
        hub.corn.CORN.osfinger = f"{hub.corn.CORN.os}-{hub.corn.CORN.osmajorrelease}"
        # In salt, osfullname was a duplicate of what osfinger should have been and osfinger didn't exist
        # It's set straight now
        hub.corn.CORN.osfullname = f"{hub.corn.CORN.os}-{hub.corn.CORN.osrelease}"
    else:
        hub.corn.CORN.osfullname = hub.corn.CORN.osfinger = hub.corn.CORN.os
