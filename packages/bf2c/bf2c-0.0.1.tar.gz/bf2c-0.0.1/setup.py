from setuptools import setup

version = '0.0.1'

setup(name='bf2c',
      version=version,
      packages=['bf2c'],
      description='Brainf*ck to C programming language converter.',
      keywords='bf brainfuck converter',
      author='Roman Stražanec',
      author_email='roman.strazanec007@gmail.com',
      license='MIT',
      url='https://github.com/romanstrazanec/bf2c',
      download_url=f'https://github.com/romanstrazanec/bf2c/releases/tag/v{version}',
      classifiers=[
          "Development Status :: 4 - Beta",
          "Environment :: Console",
          "Intended Audience :: Developers",
          "License :: OSI Approved :: MIT License",
          "Programming Language :: Python :: 3.8",
          "Topic :: Other/Nonlisted Topic"
      ]
      )
