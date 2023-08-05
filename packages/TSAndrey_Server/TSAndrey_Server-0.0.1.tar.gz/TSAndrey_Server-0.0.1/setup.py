from setuptools import setup, find_packages

setup(name="TSAndrey_Server",
      version="0.0.1",
      description="Messanger_Server",
      author="Timborevich Andrey",
      author_email="siblp@mail.ru",
      packages=find_packages(),
      install_requires=["PyQt5", "sqlalchemy", 'pycriptodome']
      )
