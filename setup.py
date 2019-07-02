import setuptools

setuptools.setup(
    name="market-game",
    version="0.0.4",
    author="William Wyatt",
    author_email="wwyatt@ucsc.edu",
    description="Market game",
    long_description="Market Game.",
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    url="https://github.com/Tsangares/market",
    scripts=['bin/business','bin/market','bin/mine','bin/transact','bin/update','bin/genProfile'],
    install_requires=[
        "aniso8601>=7.0.0",
        "Click>=7.0",
        "dnspython>=1.16.0",
        "Flask>=1.0.3",
        "Flask>PyMongo==2.3.0",
        "Flask>RESTful==0.3.7",
        "itsdangerous>=1.1.0",
        "Jinja2>=2.10.1",
        "jsonify>=0.5",
        "MarkupSafe>=1.1.1",
        "numpy>=1.16.4",
        "pymongo>=3.8.0",
        "pytz>=2019.1",
        "PyYAML>=5.1.1",
        "six>=1.12.0",
        "Werkzeug>=0.15.4",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
