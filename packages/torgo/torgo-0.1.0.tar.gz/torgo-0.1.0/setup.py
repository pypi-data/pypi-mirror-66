# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['torgo']

package_data = \
{'': ['*']}

install_requires = \
['argparse>=1.4.0,<2.0.0',
 'colorama>=0.4.3,<0.5.0',
 'configparser>=5.0.0,<6.0.0',
 'pathlib>=1.0.1,<2.0.0',
 'tinydb>=3.15.2,<4.0.0']

entry_points = \
{'console_scripts': ['torgo = torgo.torgo']}

setup_kwargs = {
    'name': 'torgo',
    'version': '0.1.0',
    'description': 'The system-wide Org file manager',
    'long_description': '<p align="center"><img src="torgo.jpg" /></p>\n\nTorgo is the system-wide org file manager. It allows you to create org-mode\nfiles that are associated with whatever directory you are in, but which are\nmanaged externally.\n\n# Usage\n\n```\nusage: torgo [-h] [-l] [-t] [-i] [-p] [command] [param]\n\nOrg-file anywhere, managed\n\npositional arguments:\n  command      The command to run\n  param        Optional param for commands, see commands list for more\n               information\n\noptional arguments:\n  -h, --help   show this help message and exit\n  -l, --list   List the commands available\n  -t, --this   Use \'this\' directory, don\'t attempt to find org file in parents\n  -i, --init   Force a re-init of the configuration\n  -p, --prune  Prune the current org file (delete it)\n```\n\nWherever you run torgo, torgo will create a managed org-mode file for the\ndirectory you are in. This org-mode file will be stored in a central location,\nbut will be associated with the directory torgo was called from.\n\n## Configuration\n\nWhen torgo is first ran, it will walk you through a configuration file\ncreation process. This configuration file defaults to `~/.torgo.cfg`, but you\ncan override that with the `$TORGO_CFG` environment variable.\n\nThe config file defines the following settings:\n\n* `org_dir` : This is the path to where your org files will go. It defaults\nto `~/.torgo/`.\n* `editor` : This is your desired text editor. If blank, will attempt to use\n`$EDITOR` from your environment.\n* `ext` : This is the desired org file extension. It defaults to `org`.\n\nYou can force torgo to re-initialize the configuration by passing the\n`-i`/`--init` option.\n\n## How does it work?\n\nPerhaps the best way to understand how to use torgo, is to see how it works.\n\nWhen torgo is run, it starts in the current working directory and checks if\nan org file entry exists for that directory in its flat database file (by\ndefault, this is `~/.torgo/org_lookup_db.json`). If no org-file is found, it\nsteps up to the parent directory and checks there. It repeats this until it\neither finds an org file or reaches root. If it reaches root, then it takes\nthe original working directory as the one for the org-mode.\n\n*Note: You can force it to use the current working directory by passing the\n`-t`/`--this` parameter.*\n\nOnce it has the appropriate org-mode file it fires up your editor of choice\non that file. You edit the file, take your notes or whatever, and save it.\n\nThe next time you fire up torgo in that same directory (or in a sub-directory)\nit will load the same org-mode file.\n\n### Tagging\n\nEach org file can be tagged with any number of tags. To set or unset the tags,\nuse the `tag` command. Tags are a comma-separated list of parameters after\nthe tag command. Tags with a `.` (period/dot) prefix will be unset. To list\nthe tags for a given org file, call tag without any parameters.\n\n```\n> torgo tag foo,bar,baz\n> torgo tag\nThe tags associated with this org file:\n    foo\n    bar\n    baz\n> torgo tag .bar\n> torgo tag\nThe tags associated with this org file:\n    foo\n    baz\n```\n\nOnce tagged, you can search for all the paths which have org files associated\nwith a given list of tags using the `search` command using a list of tags as\nits parameter.\n\n```\n> torgo search tag=foo,bar\nFound 3 records with the following tags:\n\tfoo\n\tbar\n\nPath: /home/sam/work/torgo | [oss, python, foo]\nPath: /home/sam/work/bigdeal | [bar, work]\nPath: /home/sam/meh | [oss, github, dotfiles, foo, bar]\n```\n\n### Does it have to be org-mode files?\n\nNo! Simply change the `ext` in the configuration file to whatever extension\nyou\'d like. Torgo doesn\'t force any file type on you, it just manages the\nfiles associated with your directories. If you would rather take your notes\nin Markdown, plain-text, or anything else, you\'re free to do so.\n\n# Why is it called Torgo?\n\nFor a while, I had been using a `this.org` pattern for my ad-hoc org files.\nSay I was in a directory that was a repo for a project I was on and suddenly\nneeded to take notes- I\'d do a `vim .this.org` and write my notes in it. Or\nsay I was configuring something in the system and needed to take notes on\nwhat I was doing- Again, I\'d do a `vim .this.org`.\n\nThis pattern worked well because I\'d always be able to have contextual org-mode\nnote files wherever I was. But it had a number of downsides.\n\nFor one, it littered my directories with `.this.org` files. If a directory\nwas a repo, I\'d generally have to add `.this.org` to its ignore file. Further,\nI\'d have no way to easily backup or version control all of my `.this.org` files.\n\nI created a hacky shell script that would let me have system-wide org-mode files\nin my home-directory that would be associated by hashes of the directories I\nwas in. This let me keep my `this.org` pattern, but not litter my directories.\nIt also let me version control my `this.org` files and back them up easily.\n\nOriginally, this shell script was called `torg` (from `this.org`). As I started\nrefining it, and extending it, I eventually decided I should re-write it in\nPython. Since I was a MST3k fan, and since Manos The Hands of Fate is the\ngreatest movie of all time, it was an easy leap to go from `this.org`, to `torg`,\nto `torgo`.\n',
    'author': 'Sam Hart',
    'author_email': 'hartsn@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/criswell/torgo',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
