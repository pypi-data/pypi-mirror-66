from setuptools import setup, find_packages
import sys

pkg_data = {}

if sys.platform == 'win32':
  pkg_data = {'say_something': ['SETInterfaceCS.dll','interface_cpp.hpp','interface_cpp.so','c_models.h']}

if sys.platform in ['darwin', 'linux', 'bsd', 'sunos']:
  pkg_data = {'say_something': ['SETInterfaceCS.dll','interface_cpp.hpp','interface_cpp.so','c_models.h']}

setup(
    name="say23",
    version="0.1",
    packages = find_packages(exclude = ['say_something.test']),
    package_data=pkg_data,
)