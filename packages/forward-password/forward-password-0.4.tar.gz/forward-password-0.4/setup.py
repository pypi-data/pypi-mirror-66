from setuptools import setup, find_packages

setup(name='forward-password',
      version='0.4',
      url='https://github.com/dicedtomatoreal/forward',
      license='MIT',
      author='dicedtomato',
      author_email='pranaco2@gmail.com',
      description='Manage passwords on the command line',
      packages=['forward_cli'],
      install_requires=[
          'click==7.1.1',
          'cryptography==2.9'
      ],
      entry_points={
          'console_scripts': ['forward = forward_cli.__main__:cli'],
      },
      long_description=open('README.md').read(),
      zip_safe=False
      )
