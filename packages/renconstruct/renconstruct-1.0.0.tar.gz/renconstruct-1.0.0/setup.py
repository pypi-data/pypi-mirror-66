# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['renconstruct', 'renconstruct.tasks']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.1,<8.0.0',
 'logzero>=1.5.0,<2.0.0',
 'pyyaml>=5.3.1,<6.0.0',
 'renotize>=1.0.2,<2.0.0',
 'renutil>=1.6.0,<2.0.0',
 'termcolor>=1.1.0,<2.0.0',
 'tqdm>=4.45.0,<5.0.0']

entry_points = \
{'console_scripts': ['renconstruct = renconstruct.renconstruct:cli']}

setup_kwargs = {
    'name': 'renconstruct',
    'version': '1.0.0',
    'description': "A utility script for automatically building Ren'Py applications for multiple platforms.",
    'long_description': '# renConstruct\n[![CircleCI](https://circleci.com/gh/kobaltcore/renconstruct.svg?style=svg)](https://circleci.com/gh/kobaltcore/renconstruct)\n[![Downloads](https://pepy.tech/badge/renconstruct)](https://pepy.tech/project/renconstruct)\n\nA utility script to automatically build Ren\'Py applications for multiple platforms.\n\nrenConstruct can build distributions for Windows, Linux, macOS and Android, including extra processing steps pre- and post-build.\nBy default it supports notarization for macOS distributions, a memory limit increase for Windows distributions (using `LARGEADDRESSAWARE`) and cleanup of temporary build artifacts.\n\nCustom pre- and post-build steps can easily be added.\n\n## Installation\nrenConstruct can be installed via pip:\n```bash\n$ pip install renconstruct\n```\n\nPlease note that renConstruct requires Python 3 and will not provide backwards compatibility for Python 2 for the foreseeable future.\n\n## Usage\nrenConstruct operates based on the following process flow:\n- Ensure dependencies are installed\n- Validate configuration file\n- Install specific Ren\'Py if necessary\n- Run the `pre-build` stage of all active tasks\n- Build the Android distribution if enabled\n- Build the macOS and Windows/Linux distributions if enabled\n- Run the `post-build` stage of all active tasks\n\nIn the default configuration, the following tasks are executed at the respective build stage:\n- `pre-build`:\n    + `None`\n- `post-build`:\n    + `set_extended_memory_limit`\n    + `clean`\n\n### Configuration\nrenConstruct requires a configuration file to be supplied containing the information required to complete the build process for the various platforms. An empty template is provided in this repository under the name `config.empty.yml`\n\nIt consists of the following sections:\n\n#### `tasks`\n- `path`: An optional path to a directory containing Python files with custom tasks\n- `convert_images`: A value of `true` or `false` determining whether to run this task or not\n- `set_extended_memory_limit`: A value of `true` or `false` determining whether to run this task or not\n- `notarize`: A value of `true` or `false` determining whether to run this task or not\n- `clean`: A value of `true` or `false` determining whether to run this task or not\n\n##### Custom Tasks\nCustom tasks can easily be added using the `path` value. It should point to a directory containing Python files.\nEach file can contain one or more task, which will be picked up by renConstruct.\n\nA task is an object that looks like this:\n```python\nclass DoSomethingTask():\n\n    PRIORITY = -100\n\n    def __init__(self, config):\n        self.config = config\n\n    def pre_build(self):\n        pass\n\n    def post_build(self):\n        pass\n```\n\nThe name of the class must end with `Task` for it to be picked up by renConstruct.\nEvery custom task will automatically receive a setting in the config file based on the class name split on uppercase letters, converted to lowercase and joined by underscores.\nThe example task above would receive the config variable `do_something`.\n\nA task can have two methods `pre_build` and `post_build` (either or both is possible).\nThey will be called with the validated config object at the specified build stage.\nAt that point they can do whatever they want. As an example, a custom task could be built to automatically optimize image assets in the game directory before every build.\n\nEach task also has a `PRIORITY` class attribute which has a default value of `0` and determines the order in which to run the tasks. A higher priority means that task will be executed earlier than others with a lower value. Both positive and negative values are possible.\n\nAs an example, the built-in `clean` task runs at `PRIORITY = -1000` to ensure it\'s always the last task to be run.\n\n#### `build`\n- `win`: A value of `true` or `false` determining whether to build the Windows/Linux distribution or not\n- `mac`: A value of `true` or `false` determining whether to build the macOS distribution or not\n- `android`: A value of `true` or `false` determining whether to build the Android distribution or not\n\n\n#### `renutil`\n- `version`: The version of Ren\'Py to use while building the distributions\n\n#### `renotize`\n- `apple_id`: The e-Mail address belonging to the Apple ID you want to use for signing applications.\n- `password`: An app-specific password generated through the [management portal](https://appleid.apple.com/account/manage) of your Apple ID.\n- `identity`: The identity associated with your Developer Certificate which can be found in `Keychain Access` under the category "My Certificates". It starts with `Developer ID Application:`, however it suffices to provide the 10-character code in the title of the certificate.\n- `bundle`: The internal name for your app. This is typically the reverse domain notation of your website plus your application name, i.e. `com.example.mygame`.\n- `altool_extra`: An optional string that will be passed on to all `altool` runs in all commands. Useful for selecting an organization when your Apple ID belongs to multiple, for example. Typically you will not have to touch this and you can leave it empty.\n\n### Example\n```bash\nrenconstruct -c config.yml -i path/to/my-game/ -o out/\n```\n\n### Command Line Interface\n```\nUsage: renconstruct.py [OPTIONS]\n\n  A utility script to automatically build Ren\'Py applications for multiple\n  platforms.\n\nOptions:\n  -i, --input TEXT   The path to the Ren\'Py project to build  [required]\n  -o, --output TEXT  The directory to output build artifacts to  [required]\n  -c, --config TEXT  The configuration file for this run  [required]\n  -d, --debug        If given, shows debug information if\n  --help             Show this message and exit.\n```\n\n# Disclaimer\nrenConstruct is a hobby project and not in any way affiliated with Ren\'Py. This means that there is no way I can guarantee that it will work at all, or continue to work once it does.\n',
    'author': 'CobaltCore',
    'author_email': 'cobaltcore@yandex.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kobaltcore/renconstruct',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
