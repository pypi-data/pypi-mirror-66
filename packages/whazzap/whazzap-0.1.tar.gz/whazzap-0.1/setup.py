from setuptools import setup

setup(name='whazzap',
      version='0.1',
      description='A library to treat message text import without media from WhatsApp',
      url='https://github.com/beatrizcastro89/whazzap',
      author='Beatriz Yumi Simões de Castro',
      author_email='beatrizyumi@gmail.com',
      license='MIT',
      packages=['whazzap'],
      install_requires=['pandas'],
      python_requires='>=3.6',
      zip_safe=False)