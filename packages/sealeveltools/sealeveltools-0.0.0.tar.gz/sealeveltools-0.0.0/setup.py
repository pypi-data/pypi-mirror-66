from setuptools import setup, find_packages


packages = find_packages()

setup(
    name="sealeveltools",
    version='0.0.0',
    description='A project to handle sea level data (altimetry, tide-gauges, models) and statistical exploitation tools',
    license='',
    author='Julius Oelsmann',
    author_email='julius.oelsmann@tum.de',
    packages=packages,
    url="https://gitlab.lrz.de/iulius/sea_level_tool.git"
    #package_data={    },
    #entry_points={    },
    #setup_requires=["pytest-runner"],
)

