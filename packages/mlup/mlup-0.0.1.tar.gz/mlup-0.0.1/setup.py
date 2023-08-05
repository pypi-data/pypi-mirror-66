import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "mlup", # Replace with your own username
    version = "0.0.1",
    author = "Sai Sandeep Rayanuthala",
    author_email = "rayanuthalas@gmail.com",
    description = "Automl by DSCVIT",
    entry_points = {"console_scripts" : [
                        'mlup = mlup:cli'
        ]},
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/unknown-guy-1610/mlAPI",
    packages = setuptools.find_packages(),
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['asgiref', 'astroid', 'dj-database-url', 'Django', 'django-heroku', 'djangorestframework', 'gunicorn', 'isort', 'lazy-object-proxy', 'mccabe', 'psycopg2', 'pylint', 'pytz', 'six', 'sqlparse', 'toml', 'typed-ast', 'whitenoise', 'wrapt'],
    python_requires = '>=3.6',
    
)