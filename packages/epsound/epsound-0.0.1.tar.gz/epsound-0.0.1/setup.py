from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='epsound',
      version='0.0.1',
      description='Sound player library',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/EPC-MSU/epsound',
      author='EPC MSU',
      author_email='goncharovush@physlab.ru',
      license='MIT',
      packages=['epsound'],
      install_requires=[
            'simpleaudio==1.0.4',
      ],
      classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
      ],
      python_requires='>=3.6',
      zip_safe=False)