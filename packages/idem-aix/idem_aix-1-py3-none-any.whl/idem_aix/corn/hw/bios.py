"""
Provides
    biosversion
    productname
    manufacturer
    serialnumber
    biosreleasedate
    uuid
"""
import re
import shutil


async def load_lscfg(hub):
    lscfg = shutil.which("lscfg")
    if lscfg:
        ret = await hub.exec.cmd.run([lscfg, "-vpl", "sysplanar0"])

        match = re.search("Microcode Level\.+(\S+)", ret.stdout)
        if match:
            hub.corn.CORN.biosversion = match.group(1)

        match = re.search("Microcode Build Date\.+(\S+)", ret.stdout)
        if match:
            hub.corn.CORN.biosreleasedate = match.group(1)

        match = re.search("Name:\s+(\S+)", ret.stdout)
        if match:
            hub.corn.CORN.manufacturer = match.group(1).split(",")[0]

        match = re.search("Microcode Image\.+(\S+)", ret.stdout)
        if match:
            hub.corn.CORN.productname = match.group(1)

        match = re.search("Machine/Cabinet Serial No\.+(\S+)", ret.stdout)
        if match:
            hub.corn.CORN.serialnumber = match.group(1)


async def load_uuid(hub):
    lsattr = shutil.which("lsattr")
    if lsattr:
        ret = await hub.exec.cmd.run([lsattr, "-El", "sys0"])
        match = re.search("os_uuid\s+(\S+)", ret.stdout)
        if match:
            hub.corn.CORN.uuid = match.group(1)
