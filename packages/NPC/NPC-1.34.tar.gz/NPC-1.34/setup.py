from setuptools import setup, find_packages

setup(
	name='NPC',
    version='1.34',
    description='Parallel Processing in Network Devices',
    long_description="""

# Introduction

NTP is a new parallel threading model which work in **network level**. Here two types of process work.

1. Communication
2. Execution

Here communication start using local parallel thread but the execution happens in network devices.

NPC is Network Processor Client to interface with Network Processor.
Network can be run using Virtual Machine [Tested in Oracle Virtual Box]. Download the Netowork Processor from https://ntp.perity.site/NTP.ova

# Usage

    import NPC\n
    NPC.register(ip, file_path) # ip = Machine IP Address, file_path = path to token.txt\n
    NPC.findServers() # Find for execution servers\n
    NPC.ntpExec(program,ip,timeout) # program = Code Written in Python, ip = Machine IP Address, timeout = Integer value in seconds\n
    NPC.fileTransfer(ip, file_path) # ip = Machine IP Address, file_path = path to your file\n

# Tutorial

https://ntp.perity.site/

# Pricing

https://ntp.perity.site/

# FAQ

https://ntp.perity.site/

# License

www.perity.site/slicense

    """,
    url='https://ntp.perity.site',
    author='Dipnarayan Das',
    author_email='dipnarayan.das35@gmail.com',
    install_requires=['netifaces'],
    license='License.txt',
   	packages=['NPC']
)
