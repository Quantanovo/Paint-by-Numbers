from setuptools import setup

VERSION = '0.1.0' 
DESCRIPTION = 'Paint By Numbers Creator'
LONG_DESCRIPTION = 'Convert any image into a printable paint by numbers.'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="pbn", 
        version=VERSION,
        author="Michael Pienaar",
        author_email="mpienaar9@gmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=['pbn'],
        install_requires=['matplotlib', 'sklearn', 'opencv-python', 'python-polylabel', 'numpy'], 
        keywords=['python', 'art', 'painting']
)