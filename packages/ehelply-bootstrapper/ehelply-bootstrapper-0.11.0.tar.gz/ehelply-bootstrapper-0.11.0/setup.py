from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='ehelply-bootstrapper',
    packages=find_packages(),  # this must be the same as the name above
    version='0.11.0',
    description='eHelply Bootstrapper',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Shawn Clake',
    author_email='shawn.clake@gmail.com',
    url='https://github.com/ehelply/Bootstrapper',
    keywords=[],
    include_package_data=True,
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ),
    install_requires=[
        # Packages for Drivers (Comment in/out as needed)
        'fastapi == 0.33.*',
        'pymongo == 3.8.*',
        'redis == 3.2.*',
        'python-socketio == 4.2.*',
        'sentry-asgi == 0.2.*',
        'boto3 == 1.9.*',
        'pymysql',
        'SQLAlchemy',
        'alembic',

        'wheel',

        # Packages for security (DO NOT comment these out)
        'python-jose[cryptography]',
        'pyjwt == 1.7.*',
        'passlib[bcrypt] == 1.7.*',
        'cryptography',

        # Packages for developing microservice commands (DO NOT comment these out)
        'typer',

        # Packages for release system (DO NOT comment these out)
        'GitPython',

        # Packages for runtime (DO NOT comment these out)
        'uvicorn == 0.8.*',

        # Helpful packages (Comment in/out as needed)
        'pprint == 0.1',
        'python-multipart == 0.0.*',
        'email-validator == 1.0.*',
        'requests == 2.22.*',
        'python_dateutil == 2.6.0',
        'python-slugify',
        'isodate',

        'six == 1.12.*',
        'pydantic == 0.30.*',
        'pymlconf == 1.2.*',

        # Packages for dev or testing (DO NOT comment these out)
        'pytest == 5.0.*',

        # Packages for code cleanliness (Comment in/out as needed)
        'pylint',

        # Misc eHelply Packages (Comment in/out as needed)
        'ehelply-logger >= 0.0.8',
        'ehelply-batcher >= 1.2.2',
        'ehelply-cacher >= 0.1.0',
    ],

)
