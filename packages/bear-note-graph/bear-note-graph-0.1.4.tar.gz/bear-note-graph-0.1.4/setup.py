# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bear_note_graph']

package_data = \
{'': ['*']}

install_requires = \
['colorlog>=4.1.0,<5.0.0', 'pyyaml>=5.3,<6.0']

entry_points = \
{'console_scripts': ['bear-note-graph = bear_note_graph.main:main']}

setup_kwargs = {
    'name': 'bear-note-graph',
    'version': '0.1.4',
    'description': 'Generate a graphviz visualisation of your Bear notes. It also has a partial Markdown parser, because why not',
    'long_description': '# Bear-note-graph 🐻🐍\n\n[![PyPI version](https://badge.fury.io/py/bear-note-graph.svg)](https://badge.fury.io/py/bear-note-graph)\n\n_Note_: Still WIP, not as thoroughly tested as I would have liked\n\nThis is a simple CLI to generate a [Graphviz](https://www.graphviz.org/doc/info/attrs.html)-powered graph of your notes in [Bear](https://bear.app/).\n\n## Example\n\nThis is an example in PNG format, with the flag `--anonymise`, which you can use in case you want to show your own graph but avoid showing the titles of your notes `¯\\﹍(ツ)﹍/¯`\n\n<a href="https://github.com/rberenguel/bear-note-graph/raw/master/resources/bear_graph.png" target="_blank"><img src="https://raw.githubusercontent.com/rberenguel/bear-note-graph/master/resources/bear_graph.png" alt="Example graph" width="800"></a>\n\nIf you use the default output (PDF) you will get clickable links to notes and tags (BUT ONLY ON iOS, Preview for Mac does not open app links). I recommend you copy your graph to iCloud if you want clicking. You can see an example of the PDF <a href="resources/bear_graph.pdf" target="_blank">here</a> (although it is anonymised as well).\n\n## Installation\n\nYou need an environment with at least Python 3.7, and\n\n```bash\npip install bear-note-graph\n```\n\n## Installing graphviz\n\nTo generate the graph, the `sfdp` command from Graphviz needs to be available, and for some settings (like, if you want to change overlap modes) you may need to reinstall to add `gts`. For this, you should have [homebrew](https://brew.sh) available.\n\n```bash\nbrew uninstall graphviz --ignore-dependencies\nbrew install gts\nbrew install graphviz\n```\n\n## Usage\n\n```\nusage: bear-note-graph [-h] [--config [config]] [--dump-config]\n                       [--dump-palette] [--anonymise] [--only-tags]\n                       [--only-notes] [--debug]\n\nbear-note-graph generates a Graphviz graph of your Bear notes\n\noptional arguments:\n  -h, --help         show this help message and exit\n  --config [config]  Configuration file to use. Use --dump-config-file to get\n                     a sample\n  --dump-config      Print the default configuration file and exit\n  --dump-palette     Print the default palette file and exit\n  --anonymise        Mangle the tags and link names preserving \'look\'\n  --only-tags        Show only tag links\n  --only-notes       Show only note links\n  --debug            Set logging to debug level\n```\n\nYou just need to run `bear-note-graph` after installing, by default everything will be output in `/tmp/`.\n\n## Configuration file\n\nThis is straight from the defaults\n\n```yaml\ngraph:\n  anonymise: False                         # Make the output anonymous\n  max_label_length: 50                     # Max length to show of the notes/tags\n  include_only_tags: ""                    # Generate graph only for these tags (comma separated)\n  exclude_titles: "readings,> "            # Skip all notes with titles containing this (comma separated)\n  exclude_tags: "journal,@"                # Skip all tags containing this (comma separated)\n  show_tag_edges: True                     # Whether to show tags and the linking between tags and notes\n  show_note_edges: True                    # Whether to show note edges\n  prune: False                             # Remove all notes with no tags (useful for include_only)\n  overlap: False                           # Overlap mode for nodes in the graph\n  sep: "+90,90"                            # Margins around nodes\n  splines: True                            # Whether to use splines for the arrows\n  bgcolor: "solarized-dark.base02"         # Background colour for the graph\n  free_form: "K=0.9"                       # Any additional parameters to Graphviz\n  tmp: "/tmp"                              # Temporary folder for the copy of the Bear SQLite database\n  destination: "/tmp/bear_graph"           # Default destination for the Graphviz result\n  output_format: "pdf"                     # Format of the output graphviz (only useful if run_graphviz is set)\n  run_graphviz: "sfdp"                     # Algorithm to run automatically sfdp or neato recommended\n\ntag:\n  shape: "folder"                          # Shape\n  style: "rounded,filled"                  # Style\n  fill_color: "solarized-dark.yellow"      # Fill\n  strike_color: "solarized-dark.orange"    # Stroke\n  free_form: ""\n\nnote:\n  shape: "note"\n  style: "filled"\n  fill_color: "solarized-dark.cyan"\n  strike_color: "solarized-dark.blue"\n  free_form: ""\n\ntag_link:\n  strike_color: "solarized-dark.magenta"\n  arrowhead: "none"                        # Arrowhead\n  free_form: "penwidth=\\"2.5\\""            # You can add any additional parameters\n\nnote_link:\n  strike_color: "solarized-dark.green"\n  arrowhead: "normal"\n  free_form: "penwidth=\\"2.5\\""\n\ncustom_palette_here:                       # You can inline palettes here\n  screaming_color: "#AAAAAA"               # You can inline palettes here\n```\n\nMost of the configuration parameters are for Graphviz, so check them in their [documentation](https://www.graphviz.org/doc/info/attrs.html).\n\n## The Markdown parsing\n\nIn case you are curious, I wrote a custom [Markdown parser](bear_note_graph/parser). Because, why not, and I wanted to play with parser combinators. It is not as thoroughly tested as I would like, and it also has issues with blank spaces around the nodes, but for the purpose I wanted it, it works.\n\n## The anonymisation\n\nThis is just so I can show my own graph without showing the tags or note titles. It\'s based on a relatively good hashing algorithm, and does some tweaking to make it look "realistic". \n',
    'author': 'Ruben Berenguel',
    'author_email': 'ruben+poetry@mostlymaths.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/rberenguel/bear-note-graph',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
