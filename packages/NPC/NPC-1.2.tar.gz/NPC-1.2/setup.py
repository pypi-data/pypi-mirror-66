from setuptools import setup, find_packages

setup(
	name='NPC',
    version='1.2',
    description='Parallel Processing in Network Devices',
    long_description="""
         Documentation => https://ntp.perity.site/
    """,
    url='https://ntp.perity.site',
    author='Dipnarayan Das',
    author_email='dipnarayan.das35@gmail.com',
    license='License.txt',
    py_modules=["NPC"],
   	package=['NPC'],
   	include_package_data=True,
    zip_safe=False
)
