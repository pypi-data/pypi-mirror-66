"""
Return the CPU information for Solaris-like systems
    Provides:
      cpuarch
      num_cpus
      cpu_model
      cpu_flags
"""
import asyncio
import os
import re
import shutil


async def load_cpu_arch(hub):
    isainfo = shutil.which("isainfo")
    if isainfo:
        ret = await hub.exec.cmd.run([isainfo, "-k"])
        hub.corn.CORN.cpuarch = ret.stdout.strip()
    else:
        hub.corn.CORN.cpuarch = hub.corn.CORN.get("osarch")


async def load_cpu_flags(hub):
    cpu_flags = []

    isainfo = shutil.which("isainfo")

    if isainfo:
        ret = await hub.exec.cmd.run([isainfo, "-n", "-v"])
        for line in ret.stdout.splitlines():
            match = re.match(r"^\s+(.+)", line)
            if match:
                cpu_flags.extend(match.group(1).split())

    hub.corn.CORN.cpu_flags = sorted(set(cpu_flags))

    # Report if hardware virtualization is available under amd or intel
    hub.corn.CORN.hardware_virtualization = any(
        f in hub.corn.CORN.cpu_flags for f in ("svm", "vmx")
    )


async def load_cpu_model(hub):
    kstat = shutil.which("kstat")
    ret = await hub.exec.cmd.run([kstat, "-p", "cpu_info:*:*:brand"], shell=True)
    for line in ret.stdout.splitlines():
        match = re.match(r"(\w+:\d+:\w+\d+:\w+)\s+(.+)", line)
        if match:
            hub.corn.CORN.cpu_model = match.group(2)
            break


async def load_num_cpus(hub):
    psrinfo = shutil.which("psrinfo") or "/usr/sbin/psrinfo"
    if os.path.exists(psrinfo):
        ret = await hub.exec.cmd.run(psrinfo, stderr=asyncio.subprocess.DEVNULL)
        hub.corn.CORN.num_cpus = len(ret.stdout.strip().splitlines())
