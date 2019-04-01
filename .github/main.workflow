workflow "Run Tests" {
  on = "push"
  resolves = ["Lint"]
}

action "Lint" {
  uses = "docker://python:3.6"
  args = "pip install tox coveralls && tox -e lint"
}

action "py27-dj111" {
  uses = "docker://python:2.7"
  needs = ["Lint"]
  args = "pip install tox coveralls && tox -e py27-dj111"
}

action "py36-dj111" {
  uses = "docker://python:3.6"
  needs = ["Lint"]
  args = "pip install tox coveralls && tox -e py36-dj111 && coveralls"
}

action "py36-dj20" {
  uses = "docker://python:3.6"
  needs = ["Lint"]
  args = "pip install tox coveralls && tox -e py36-dj20 && coveralls"
}

action "py36-dj21" {
  uses = "docker://python:3.6"
  needs = ["Lint"]
  args = "pip install tox coveralls && tox -e py36-dj21 && coveralls"
}

action "py36-dj22" {
  uses = "docker://python:3.6"
  needs = ["Lint"]
  args = "pip install tox coveralls && tox -e py36-dj22 && coveralls"
}

workflow "Publish" {
  on = "release"
  resolves = ["Publish to PyPI", "Publish docs"]
}

action "Publish to PyPI" {
  uses = "docker://python:3.6"
  secrets = ["TWINE_USERNAME", "TWINE_PASSWORD"]
  args = "pip install --upgrade setuptools wheel twine && python setup.py sdist bdist_wheel --universal && twine upload --repository-url https://test.pypi.org/legacy/ dist/*"
}

action "Publish docs" {
  uses = "docker://python:3.6"
  args = "pip install '.[docs]' && mkdocs gh-deploy"
}
