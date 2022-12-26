from setuptools import find_packages, setup

from pylama_dmypy import VERSION

# fmt: off

setup(
      name = "pylama-dmypy"
    , version = VERSION
    , packages = find_packages(include="pylama_dmypy.*", exclude=["tests*"])

    , extras_require =
      { 'tests':
        [ "pylama==8.3.8"
        , "mypy==0.942"
        ]
      }

    , entry_points =
      { 'pylama.linter': ['dmypy = pylama_dmypy.linter:Linter']
      }

    # metadata
    , url = "http://github.com/delfick/pylama_dmypy"
    , author = "Stephen Moore"
    , author_email = "stephen@delfick.com"
    , description = "Linting plugin for pylama to see dmypy"
    , long_description = open("README.rst").read()
    , license = "MIT"
    )

# fmt: on
