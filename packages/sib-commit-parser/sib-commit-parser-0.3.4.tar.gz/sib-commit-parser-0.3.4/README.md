# StartinBlox commit message parser

This pakage implements the releasing policy of SIB project based on commit messages.

[See reference](https://git.happy-dev.fr/startinblox/management#commit-messages)

## Setup

Add the relevant `semantic_release` section to your `setup.cfg`:
```
[semantic_release]
version_source = tag
version_variable = myapp/__init__.py:__version__
commit_parser = commit_parse.parse
```

## Develop the parser

Install `python-semantic-release` along with the parser:
```
# docker run --rm -v $PWD:/code -w /code -it python:3.6 bash
# pip install python-semantic-release
# pip install -e .[dev]
# export PYTHONPATH=/code/commit_parser/
```

Create a dummy project:
```
# git init /tmp/test
# cd !$
```

Add a minimal project:
```
# echo 'setup()' > setup.py
# echo '__version__ = 0.0.0' > version.py
# cat <<EOF > setup.cfg
[semantic_release]
upload_to_pypi = false
version_source = tag
version_variable = version.py:__version__
commit_parser = commit_parser.parse
EOF
```

Simulate release:
```
# git commit --allow-empty -m 'fix: some stupid message'
# semantic-release version --noop
Creating new version.
Current version: 0.0.0
No operation mode. Should have bumped from 0.0.0 to 0.0.1.
```

Use `# DEBUG=semantic_release:* semantic-release version --noop` to see debug messages.
