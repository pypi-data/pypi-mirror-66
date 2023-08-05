from setuptools import setup, find_packages

setup(name='evohomeclient-mnbf9rca',
      version='0.1',
      description='A simple evohome client',
      url='https://github.com/mnbf9rca/EvohomeClient',
      author='mnbf9rca',
      author_email='robert.aleck@cynexia.com',
      license='MIT',
      packages=find_packages(),
      install_requires=[
          'requests',
          'python-dotenv',
          'python-dateutil'
      ],
      zip_safe=False,
      python_requires='>=3.6')