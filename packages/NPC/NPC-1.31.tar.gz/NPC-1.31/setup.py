from setuptools import setup, find_packages

setup(
	name='NPC',
    version='1.31',
    description='Parallel Processing in Network Devices',
    long_description="""
NTP is a new parallel threading model which work in network level. Here two types of process work.\n
1. Communication\n
2. Execution\n\n
Here communication start using local parallel thread but the execution happens in network devices.\n\n

Language Dependency:\n
Python\n\n

Usage:\n
import NPC\n\n
NPC.register(ip, file_path)
NPC.findServers()\n
Finding for execution servers\n
==> [REGISTRATION-TYPE] [CPU-MEMORY INFORMATION] [IP-ADDRESS]\n\n
NPC.ntpExec(program,ip,timeout)
NPC.fileTransfer(ip, file_path)

Full Setup Tutorial => https://ntp.perity.site/

FAQ\n


    """,
    url='https://ntp.perity.site',
    author='Dipnarayan Das',
    author_email='dipnarayan.das35@gmail.com',
    install_requires=['netifaces'],
    license='License.txt',
   	packages=['NPC']
)
