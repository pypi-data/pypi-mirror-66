# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ofxcloudsync', 'ofxcs']

package_data = \
{'': ['*']}

install_requires = \
['OrcFxAPI==11.0.2',
 'PyYAML==5.3.1',
 'appdirs>=1.4.3,<2.0.0',
 'awscli==1.18.31',
 'boto3==1.12.30',
 'click==7.1.1',
 'cryptography>=2.9,<3.0',
 'pytest-mock>=3.0.0,<4.0.0',
 'pytest==5.4.1']

entry_points = \
{'console_scripts': ['ofxcs = ofxcs:ofxcs']}

setup_kwargs = {
    'name': 'orcaflex-cloudsync',
    'version': '0.2.3',
    'description': 'Tool to sync OrcaFlex simulations to the cloud and local drives',
    'long_description': "# OFX Cloud Sync\n\nTool which allows syncing of OrcaFlex simulation files to the cloud and back to local drives.\n\n## Requirements\n\nTo use this you will need:\n\n1. Python 3.6+ installed on all servers and local machines\n2. Cloud Key ID, Secret and Bucket (these can either be from your own [AWS account](https://aws.amazon.com/premiumsupport/knowledge-center/create-and-activate-aws-account/) or [you can request some from us](mailto:ofxcs@agiledat.co.uk?subject=Request%20for%20ofx-cloudsync%20keys&body=Hi.%20I'd%20like%20to%20be%20able%20to%20use%20this%20cool%20OrcaFlex%20cloud%20sync%20tool.)) \n\n\n## Installing\n\n\n### Using pip\n\n```bash\npip install orcaflex-cloudsync\n```\n\n## User guide\n\n### Introduction\n\nThis tool tries to solve the problem of running OrcaFlex simulations on remote servers but then wanting to have the simulation files on a local machine for viewing/processing. There are a few reasons you might want this:\n\n- remote desktop wars with other users\n- corporate VPN making everything terrible\n- cloud servers within a private network with no remote access\n\nOur solution to this comes in the form of a command line tool called `ofxcs` combined with a [post calculation action](https://www.orcina.com/webhelp/OrcaFlex/Content/html/Generaldata,Postcalculationactions.htm) script in OrcaFlex.\n\n### Configuring\n\nIf you have successfully installed the tool with pip then you should be able to type:\n\n```commandline\nofxcs\n```\n\nand see something like:\n\n```\nUsage: ofxcs [OPTIONS] COMMAND1 [ARGS]... [COMMAND2 [ARGS]...]...\n\n  Command line interface to orcaflex-cloudsync.\n\nOptions:\n  --version  Show the version and exit.\n  --help     Show this message and exit.\n\nCommands:\n  add        add a folder to sync\n  configure  configures orcaflex-cloudsync\n  keygen     generates a keyfile used to encrypt simulation data\n  remove     stop syncing a folder\n  show       shows the current config\n  sync       sync files from cloud to local drive\n\n\n```\n\n### Configuring\n\n> YOU WILL NEED TO INSTALL AND CONFIGURE ON EVERY MACHINE THAT YOU WANT TO RUN SIMULATIONS OR SYNC SIMULATIONS LOCALLY\n\n\nThe `ofxcs` tool will guide you through configuration:\n\n```commandline\nofxcs configure\n```\n\nWill ask a series of questions:\n\n1. It will ask you to enter your cloud key details, bucket and the region that your bucket is based in\n2. It will ask you where you want to copy the post calculation action script. You will need to point to this from all your models\n3. It will ask where you want to save local simulations when they are synced back to your local drive\n4. It will ask you if you have a key file. See [section below](#Encryption) for more details.\n\n### Encryption\n\nAccess to your bucket is restricted only to people who have access to the cloud key and secret and the administrator of the cloud account. Encryption allows you to ensure that your stored simulation files can only ever be read by people in your company.\n\nThis is done with a `key file`, you can generate these with:\n\n```commandline\nofxcs keygen\n``` \n\n\nThis will save a key file and optionally it will update the local config to point to the key file. \n\n> **IMPORTANT**: You should only do this once for your company and then share the key file internally and have each user configure their system with this key file. If you lose the key file there will be no way to decrypt the simulation files stored in the cloud. \n\nNow you have configured `ofxcs` you can start to sync simulations to the cloud. \n\n### Post-calculation actions\n\nIn every model you want to sync you must specify a [Post calculation action](https://www.orcina.com/webhelp/OrcaFlex/Content/html/Generaldata,Postcalculationactions.htm). Action type needs to be `In-process Python` and version must be `Python 3`.\n\n\n__The Script File Name is wherever you saved the file during the `ofxcs configure` process above.__\n\n\n> __NOTE__: The default location for `pca_ofx2cloud.py` is based on your local user profile and may be different on remote computers. It might be easier to move the file to somewhere like C:\\pca_ofx2cloud.py so it will be consistent on all machines.\n\nYou also need to add a tag on General of `FOLDER` in every model. This is how your simulations will be organised in the cloud. The folder name can contain only alphanumeric and the following special characters:\n\n```text\n! - _ . * ' ( )\n```\n\n\nWith `ofxcs` configured and post calculations specified, simulations run in batch processing or distributed OrcaFlex will be automatically uploaded to the cloud. \n\n### Local sync\n\nNow you want to sync them to you local machine. You start by adding the folders that you specified in the models:\n\n```commandline\nofxcs add --folder my_ofx_project\n```\n\nThere is no need to add the folders every time you start the sync, it will remember which folders you want.\n\nYou can then run the sync command:\n\n```commandline\nofxcs sync\n```\n\nThe syncing operation will continue until you stop it by killing the process or pressing `CRTL+C`.\n\nIf you want to see what folders are currently set to sync:\n\n```commandline\nofxcs show\n```\n\n```\n{'bucket': 'xxx000',\n 'root_folder': 'C:\\\\Users\\\\username\\\\AppData\\\\Local\\\\agiletek\\\\ofx-cloudsync\\\\ofxsync',\n 'sync': ['my_ofx_project']}\n```\n\nTo remove a folder (stop syncing it)\n\n```commandline\nofx remove --folder my_ofx_project\n```\n\nwill stop syncing but not delete the local files, whereas:\n\n```commandline\nofxcs remove --delete --folder my_ofx_project\n```\n\ndeletes the folder locally.\n\n\n## Roadmap\n\nNext steps for development:\n\n1. Proper logging\n2. Simple GUI\n\n## Help/support\n\nIf you have any questions or need any help with this package then contact [ofxcs@agiledat.co.uk](mailto:ofxcs@agiledat.co.uk)",
    'author': 'AgileDat',
    'author_email': 'ofxcs@agiledat.co.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
