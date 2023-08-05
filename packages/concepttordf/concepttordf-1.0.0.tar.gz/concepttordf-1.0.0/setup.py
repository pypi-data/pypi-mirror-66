# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['concepttordf']

package_data = \
{'': ['*']}

install_requires = \
['rdflib-jsonld>=0.5.0,<0.6.0', 'rdflib>=5.0.0,<6.0.0']

extras_require = \
{':python_version < "3.8"': ['importlib_metadata>=1.5.0,<2.0.0']}

setup_kwargs = {
    'name': 'concepttordf',
    'version': '1.0.0',
    'description': 'A library for mapping a concept collection to rdf',
    'long_description': '![Tests](https://github.com/Informasjonsforvaltning/concepttordf/workflows/Tests/badge.svg)\n[![codecov](https://codecov.io/gh/Informasjonsforvaltning/concepttordf/branch/master/graph/badge.svg)](https://codecov.io/gh/Informasjonsforvaltning/concepttordf)\n[![PyPI](https://img.shields.io/pypi/v/concepttordf.svg)](https://pypi.org/project/concepttordf/)\n[![Read the Docs](https://readthedocs.org/projects/concepttordf/badge/)](https://concepttordf.readthedocs.io/)\n# concepttordf\n\nA small Python library for mapping a concept collection to the [skos-ap-no specification](https://doc.difi.no/data/begrep-skos-ap-no/).\n\n## Usage\n### Install\n```\n% pip install concepttordf\n```\n### Getting started\nTo create a SKOS-AP-NO concept collection:\n```\nfrom concepttordf import Collection, Concept, Definition\n\n# Create collection object\ncollection = Collection()\ncollection.identifier = "http://example.com/collections/1"\ncollection.name = {"en": "A concept collection"}\ncollection.name = {"nb": "En begrepssamling"}\ncollection.publisher = "https://example.com/publishers/1"\n\n# Create a concept:\nc = Concept()\nc.identifier = "http://example.com/concepts/1"\nc.term = {"name": {"nb": "inntekt", "en": "income"}}\ndefinition = Definition()\ndefinition.text = {"nb": "ting man skulle hatt mer av",\n                   "en": "something you want more of"}\nc.definition = definition\n\n# Add concept to collection:\ncollection.members.append(c)\n\n# get rdf representation in turtle (default)\nrdf = collection.to_rdf()\nprint(rdf.decode())\n```\nWill print the concept according to the specification:\n```\n@prefix dcat: <http://www.w3.org/ns/dcat#> .\n@prefix dct: <http://purl.org/dc/terms/> .\n@prefix ns1: <https://data.norge.no/vocabulary/skosno#> .\n@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .\n@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n@prefix skos: <http://www.w3.org/2004/02/skos/core#> .\n@prefix skosno: <http://difi.no/skosno> .\n@prefix skosxl: <http://www.w3.org/2008/05/skos-xl#> .\n@prefix vcard: <http://www.w3.org/2006/vcard/ns#> .\n@prefix xml: <http://www.w3.org/XML/1998/namespace> .\n@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .\n\n<http://example.com/collections/1> a skos:Collection ;\n    rdfs:label "En begrepssamling"@nb ;\n    dct:publisher <https://example.com/publishers/1> ;\n    skos:member <http://example.com/concepts/1> .\n\n<http://example.com/concepts/1> a skos:Concept ;\n    ns1:betydningsbeskrivelse [ a ns1:Definisjon ;\n            rdfs:label "something you want more of"@en,\n                "ting man skulle hatt mer av"@nb ] ;\n    skosxl:prefLabel [ a skosxl:Label ;\n            skosxl:literalForm "income"@en,\n                "inntekt"@nb ] .\n\n```\n\n## Development\n### Requirements\n- [pyenv](https://github.com/pyenv/pyenv) (recommended)\n- [poetry](https://python-poetry.org/)\n- [nox](https://nox.thea.codes/en/stable/)\n\n### Install\n```\n% git clone https://github.com/Informasjonsforvaltning/concepttordf.git\n% cd concepttordf\n% pyenv install 3.8.2\n% pyenv install 3.7.6\n% pyenv local 3.8.2 3.7.6\n% poetry install\n```\n### Run all tests\n```\n% nox\n```\n### Run all tests with coverage reporting\n```\n% nox -rs tests\n```\n### Debugging\nYou can enter into [Pdb](https://docs.python.org/3/library/pdb.html) by passing `--pdb` to pytest:\n```\nnox -rs tests -- --pdb\n```\nYou can set breakpoints directly in code by using the function `breakpoint()`.\n',
    'author': 'Stig B. Dørmænen',
    'author_email': 'stigbd@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Informasjonsforvaltning/concepttordf',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
