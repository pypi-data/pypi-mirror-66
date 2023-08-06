# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bpaingest',
 'bpaingest.handlers',
 'bpaingest.libs',
 'bpaingest.projects',
 'bpaingest.projects.amdb',
 'bpaingest.projects.barcode',
 'bpaingest.projects.gap',
 'bpaingest.projects.gbr',
 'bpaingest.projects.melanoma',
 'bpaingest.projects.omg',
 'bpaingest.projects.sepsis',
 'bpaingest.projects.stemcells',
 'bpaingest.projects.wheat_cultivars',
 'bpaingest.projects.wheat_pathogens_genomes',
 'bpaingest.projects.wheat_pathogens_transcript']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.9.0,<5.0.0',
 'boto3>=1.12.45,<2.0.0',
 'bpasslh>=2.1.0,<3.0.0',
 'ckanapi>=4.3,<5.0',
 'google-api-python-client>=1.8.2,<2.0.0',
 'python-dateutil>=2.8.1,<3.0.0',
 'requests>=2.23.0,<3.0.0',
 'unipath>=1.1,<2.0',
 'xlrd>=1.2.0,<2.0.0',
 'xlwt>=1.3.0,<2.0.0']

entry_points = \
{'console_scripts': ['bpa-ingest = bpaingest.cli:main']}

setup_kwargs = {
    'name': 'bpaingest',
    'version': '6.4.2',
    'description': 'Data management for Bioplatforms Australia projects',
    'long_description': '# Bioplatforms Australia: CKAN ingest and sync\n\n## Usage\n\nPrimary usage information is contained in the comments at the\ntop of the ```ingest/ingest.sh``` script, which is the gateway\nto synchronising the archive.\n\n## Generating CKAN schemas\n\n`bpa-ingest` can generate `ckanext-scheming` schemas.\n\nUsage:\n\n```\n$ bpa-ingest -p /tmp/ingest/ makeschema\n```\n\n## Tracking metadata\n\nTwo types of tracking metadata are stored within this repository.\n\n### Google Drive metadata\n\nThe source of truth is "BPA Projects Data Transfer Summary", shared\nwith BPA in Google Drive. This is maintained by the various project\nmanagers.\n\nTo update, use "File", "Download as", "CSV" within Google Sheets \nand replace the CSV sheets in `track-metadata/google-drive`\n\n### BPAM metadata\n\nThe source of truth is the BPA Metadata app.\n\nTo update, export each of the tracking datasets as CSV using the\nexport button, then replace the files in `track-metadata/bpam`\n\n - https://data.bioplatforms.com/bpa/adminsepsis/genomicsmiseqtrack/\n - https://data.bioplatforms.com/bpa/adminsepsis/genomicspacbiotrack/\n - https://data.bioplatforms.com/bpa/adminsepsis/metabolomicslcmstrack/\n - https://data.bioplatforms.com/bpa/adminsepsis/proteomicsms1quantificationtrack/\n - https://data.bioplatforms.com/bpa/adminsepsis/proteomicsswathmstrack/\n - https://data.bioplatforms.com/bpa/adminsepsis/transcriptomicshiseqtrack/\n\n## AWS Lambda\n\nWe are gradually adding AWS Lambda functions to this project.\n\nEach Lambda Function will have a `handler()` function which acts as an\nentrypoint. These are being collected in `bpaingest/handlers/`\n\nLambda functions should load their configuration from S3, from a bucket and \nkey configured via environment variables. This configuration should be configured\nusing AWS KMS. The Lambda function can be granted privileges to decrypt the\nconfiguration once it has been read from S3.\n\nTo store encrypted data at a key, this pattern works\n\n    $ aws kms encrypt --key-id <key> --plaintext fileb://config.json --output text --query CiphertextBlob | base64 --decode > config.enc\n    $ aws s3 cp config.enc s3://bucket/key\n\n\n## Local development:\nFor the development environment, you will need to have your local dev environment for bpa-ckan (consider dockercompose-bpa-ckan to do this).\n\nBefore you start, ensure you have installed Python 3.7\n\nBpa-ingest, atm, is just a python virtualenv (on command line),so to initialise a dev working environment:\n```\ncd bpa-ingest\ngit checkout next_release\ngit pull origin next_release\npython3 -m venv ~/.virtual/bpa-ingest\n. ~/.virtual/bpa-ingest/bin/activate\npip install -r requirements.txt\npython setup.py install\npython setup.py develop\n```\n\nThen (ensuring that you are still in python virtual env) source the environment variables (including API key), before running the ingest:\n```\n# if not already in virtual env:\n. ~/.virtual/bpa-ingest/bin/activate\n\n# source the environment variables\n. /path/to/your/bpa.env\n\n# dump the target state of the data portal to a JSON file for one data type\nbpa-ingest -p /tmp/dump-metadata/ dumpstate test.json --dump-re \'omg-genomics-ddrad\'\n\n```\n\nLook in /tmp/dump-metadata/ and you will see the working set of metadata sources used by the tool.\nRemember to delete the contents of /tmp (or subdirectory you are dumping too), when re-running command:\n```\nrm -Rf ./tmp/\n```',
    'author': 'Grahame Bowland',
    'author_email': 'grahame.bowland@qcif.edu.au',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
