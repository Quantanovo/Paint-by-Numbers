from setuptools import setup

VERSION = '0.0.6' 
DESCRIPTION = 'Paint By Numbers Creator'
LONG_DESCRIPTION = 'Convert any image into a printable paint by numbers.'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="paint-by-numbers", 
        version=VERSION,
        author="Michael Pienaar",
        author_email="mpienaar9@gmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=['paint-by-numbers'],
        install_requires=['matplotlib', 'sklearn', 'opencv-python', 'python-polylabel', 'numpy'], 
        keywords=['python', 'art', 'painting']
)