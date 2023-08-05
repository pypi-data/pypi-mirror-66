# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['instamatic',
 'instamatic.TEMController',
 'instamatic.calibrate',
 'instamatic.camera',
 'instamatic.config',
 'instamatic.config.scripts',
 'instamatic.experiments',
 'instamatic.experiments.autocred',
 'instamatic.experiments.cred',
 'instamatic.experiments.cred_gatan',
 'instamatic.experiments.cred_tvips',
 'instamatic.experiments.red',
 'instamatic.experiments.serialed',
 'instamatic.formats',
 'instamatic.gui',
 'instamatic.neural_network',
 'instamatic.processing',
 'instamatic.server',
 'instamatic.utils']

package_data = \
{'': ['*'],
 'instamatic.camera': ['tpx/*'],
 'instamatic.config': ['alignments/*',
                       'calibration/*',
                       'camera/*',
                       'microscope/*']}

install_requires = \
['comtypes>=1.1.7',
 'h5py>=2.10.0',
 'ipython>=7.11.1',
 'lmfit>=1.0.0',
 'matplotlib>=3.1.2',
 'mrcfile>=1.1.2',
 'numpy>=1.17.3',
 'pandas>=0.25.3',
 'pillow>=7.0.0',
 'pyserialem>=0.1.0,<0.2.0',
 'pywinauto>=0.6.8',
 'pyyaml>=5.3',
 'scikit-image>=0.16.2',
 'scipy>=1.3.2',
 'tifffile>=2019.7.26.2',
 'tqdm>=4.41.1',
 'virtualbox>=2.0.0']

entry_points = \
{'console_scripts': ['instamatic = instamatic.main:main',
                     'instamatic.VMserver = '
                     'instamatic.server.vm_ubuntu_server:main',
                     'instamatic.autoconfig = '
                     'instamatic.config.autoconfig:main',
                     'instamatic.browser = scripts.browser:main',
                     'instamatic.calibrate_beamshift = '
                     'instamatic.calibrate.calibrate_beamshift:main_entry',
                     'instamatic.calibrate_directbeam = '
                     'instamatic.calibrate.calibrate_directbeam:main_entry',
                     'instamatic.calibrate_stage_lowmag = '
                     'instamatic.calibrate.calibrate_stage_lowmag:main_entry',
                     'instamatic.calibrate_stage_mag1 = '
                     'instamatic.calibrate.calibrate_stage_mag1:main_entry',
                     'instamatic.camera = instamatic.camera.camera:main_entry',
                     'instamatic.camserver = instamatic.server.cam_server:main',
                     'instamatic.controller = '
                     'instamatic.TEMController.TEMController:main_entry',
                     'instamatic.defocus_helper = '
                     'instamatic.gui.defocus_button:main',
                     'instamatic.dialsserver = '
                     'instamatic.server.dials_server:main',
                     'instamatic.find_crystals = '
                     'instamatic.processing.find_crystals:main_entry',
                     'instamatic.flatfield = '
                     'instamatic.processing.flatfield:main_entry',
                     'instamatic.goniotoolserver = '
                     'instamatic.server.goniotool_server:main',
                     'instamatic.learn = scripts.learn:main_entry',
                     'instamatic.serialed = '
                     'instamatic.experiments.serialed.experiment:main',
                     'instamatic.stretch_correction = '
                     'instamatic.processing.stretch_correction:main_entry',
                     'instamatic.temserver = instamatic.server.tem_server:main',
                     'instamatic.temserver_fei = '
                     'instamatic.server.TEMServer_FEI:main',
                     'instamatic.viewer = scripts.viewer:main',
                     'instamatic.xdsserver = '
                     'instamatic.server.xds_server:main']}

setup_kwargs = {
    'name': 'instamatic',
    'version': '1.3.0',
    'description': 'Python program for automated electron diffraction data collection',
    'long_description': '![build](https://github.com/stefsmeets/instamatic/workflows/build/badge.svg)\n![PyPI](https://img.shields.io/pypi/v/pyserialem.svg?style=flat)\n[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.1090388.svg)](https://doi.org/10.5281/zenodo.1090388)\n\n# Instamatic\n\nInstamatic is a Python program that is being developed with the aim to automate the collection of electron diffraction data. At the core is a Python library for transmission electron microscope experimental control with bindings for the JEOL/FEI microscopes and interfaces to the gatan/timepix/tvips cameras. Routines have been implemented for collecting serial electron diffraction (serialED), continuous rotation electron diffraction (cRED), and stepwise rotation electron diffraction (RED) data.\n\nInstamatic is distributed as a portable stand-alone installation that includes all the needed libraries from: https://github.com/stefsmeets/instamatic/releases. However, the most up-to-date version of the code (including bugs!) is available from this repository.\n\nElectron microscopes supported:\n\n- JEOL microscopes with the TEMCOM library\n- FEI microscopes via the scripting interface\n\nCameras supported:\n\n- ASI Timepix (including live-view GUI)\n- Gatan cameras through DM plugin\n- TVIPS cameras through EMMENU4 API\n\nInstamatic has been extensively tested on a JEOL-2100 with a Timepix camera, and is currently being developed on a JEOL-1400 and JEOL-3200 with TVIPS cameras (XF416/F416).\n\nA DigitalMicrograph script for collecting cRED data on a OneView camera (or any other Gatan camera) can be found at [dmscript](https://github.com/stefsmeets/InsteaDMatic).\n\n## Reference\n\nIf you find this software useful, please consider citing one of the references below and/or refer to the source code in your publications:\n\n- S. Smeets, B. Wang, M.O. Cichocka, J. Ångström, and W. Wan, (2018, December 7). Instamatic (Version 1.0.0). Zenodo. http://doi.org/10.5281/zenodo.2026774\n\nSome of the methods implemented in Instamatic are described in:\n\n- B. Wang, X. Zou, and S. Smeets, [Automated serial rotation electron diffraction combined with cluster analysis: an efficient multi-crystal workflow for structure determination](https://doi.org/10.1107/S2052252519007681), IUCrJ (2019). 6, 1-14\n\n- M.O. Cichocka, J. Ångström, B. Wang, X. Zou, and S. Smeets, [High-throughput continuous rotation electron diffraction data acquisition via software automation](http://dx.doi.org/10.1107/S1600576718015145), J. Appl. Cryst. (2018). 51, 1652–1661\n\n- S. Smeets, X. Zou, and W. Wan, [Serial electron crystallography for structure determination and phase analysis of nanocrystalline materials](http://dx.doi.org/10.1107/S1600576718009500), J. Appl. Cryst. (2018). 51, 1262–1273\n\n## Documentation\n\nSee [the documentation](docs) for how to set up and use Instamatic.\n\n- [TEMController](docs/tem_api.md)\n- [Config](docs/config.md)\n- [Reading and writing image data](docs/formats.md)\n- [Setting up instamatic](docs/setup.md)\n- [Programs included](docs/programs.md)\n- [GUI and Module system](docs/gui.md)\n\nUse `pydoc` to access the full API reference: `pydoc -b instamatic`\n\n## Installation\n\nThe simplest way is to download the portable installation with all libraries/dependencies included: https://github.com/stefsmeets/instamatic/releases/latest. Extract the archive, and open a terminal by double-clicking `start_Cmder.exe`.\n\nAlternatively, the latest development version can always be obtained via:\n\n    https://github.com/stefsmeets/instamatic/archive/master.zip\n\nTo install:\n\n    pip install -r requirements.txt\n    python setup.py install\n\nOr:\n\n     pip install git+https://github.com/stefsmeets/instamatic.git\n',
    'author': 'Stef Smeets',
    'author_email': 's.smeets@tudelft.nl',
    'maintainer': 'Stef Smeets',
    'maintainer_email': 's.smeets@tudelft.nl',
    'url': 'http://github.com/stefsmeets/instamatic',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
