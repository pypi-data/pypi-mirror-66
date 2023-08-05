from setuptools import setup, find_packages

setup(name="FDmitry_Client",
      version="1.0.1",
      description="Messenger-Client",
      author="Fatykov_Dmitrii",
      author_email="FDmitry82@mail.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome']
      )
