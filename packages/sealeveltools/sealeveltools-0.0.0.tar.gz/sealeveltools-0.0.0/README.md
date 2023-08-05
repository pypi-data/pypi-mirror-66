## Baltic+ Analysis

If you are a developer of this project, please not:

1) Data Files shall be placed in dataset_lfs and tracked by lfs (see below for installation)  

2) Functions from other projects shall be imported as python packages (see tutorials: https://timothybramlett.com/How_to_create_a_Python_Package_with___init__py.html) and explicit the dependency in the environment file, 

    $ for example - pip:
        - git+https://gitlab.lrz.de/dgfi-tum/python-openadb.git@master#egg=OpenADB





## Prerequisites

### Linux

Install git

    $ sudo apt install git

Install git-lfs (large file storage)

    $ curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | sudo bash
    $ sudo apt install git-lfs

Install miniconda

    $ wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
    $ bash Miniconda3-latest-Linux-x86_64.sh

### Windows

Download and install git from [here](https://git-scm.com/downloads).

Download and install git-lfs (large file storage (LFS)) from [here](https://git-lfs.github.com/).

Download and install Miniconda from [here](https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe).


## Getting started

First, clone this repository:

    $ git clone https://gitlab.lrz.de/ne62rut/balticplus.git

Go into newly created directory, to which the repository was cloned

    $ cd balticplus

Download the LFS files that are stored using git-lfs

    $ git lfs pull

--> takes some time

Then, create a virtual environment using conda

    $ conda env create

-> This install all the dependencies/packages/python-version (including version numbers) that are set in environment.yml

Switch to into the newly created, "isolated" virtual environment:

    $ conda activate balticplus
(this has to be done every time in order to work with this environment)


## Usage

