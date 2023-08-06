from setuptools import setup

setup(name='django-tiny-util',
      version='0.2.1',
      description='Useful Django utils',
      url='https://github.com/olegbo/django-tiny-util',
      author='Oleg Bogumirski',
      author_email='reg@olegb.ru',
      license='MIT',
      packages=['djangotinyutil'],
      zip_safe=True,
      classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
      ],
      python_requires='>=3.6',
      )
