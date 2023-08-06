from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('requirements.txt') as requirements_file:
    requirements = requirements_file.readlines()

setup(name='r53-register',
      author='awk',
      author_email='self@awk.space',
      version='0.1.4',
      description='Register your host IP address with Amazon Route 53.',
      long_description=readme,
      long_description_content_type='text/markdown',
      license='MIT',
      url='https://github.com/awkspace/r53-register',
      install_requires=requirements,
      packages=find_packages(),
      entry_points={
          'console_scripts': [
              'r53-register = r53_register.cli:main'
          ]
      })
