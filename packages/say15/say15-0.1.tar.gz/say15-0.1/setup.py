from setuptools import setup, find_packages
import sys

#ext_data = {}
#
#if sys.platform == 'win32':
#  ext_data = ["say_sorry", "say_sorry.py"]
#
#if sys.platform in ['darwin', 'linux', 'bsd', 'sunos']:
#  ext_data = ["say_hello", "say_hello.py"]

setup(
    name="say15",
    version="0.1",
    packages = find_packages(exclude = ["*.test", "*.test.*", "test.*", "test"]),
    package_data={'say_something': ['SETInterfaceCS.dll','interface_cpp.hpp','interface_cpp.so','c_models.h']},
)