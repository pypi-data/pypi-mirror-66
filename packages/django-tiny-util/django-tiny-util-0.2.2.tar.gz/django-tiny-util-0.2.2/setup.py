from setuptools import setup

setup(name='django-tiny-util',
      version='0.2.2',
      description='Useful Django utils',
      url='https://github.com/olegbo/django-tiny-util',
      author='Oleg Bogumirski',
      author_email='reg@olegb.ru',
      license='MIT',
      packages=['djangotinyutil'],
      install_requires=[
          'django',
      ],
      zip_safe=False,
      classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
      ],
      python_requires='>=3.6',
      )
