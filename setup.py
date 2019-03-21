from setuptools import setup


def fetch_version():
      '''
      Fetches version variable from version.py
      '''
      version = {}

      with open('pranked/version.py') as f:
            exec(f.read(), version)

      return version['__version__']



setup(name='pranked',
      version=fetch_version(),
      description='Pranking Script',
      url='http://github.com/UCLeuvenLimburg/pranked',
      author='Frederic Vogels',
      author_email='frederic.vogels@ucll.be',
      license='MIT',
      install_requires=['keyboard'],
      packages=['pranked'],
      entry_points = {
            'console_scripts': [ 'pranked=pranked.command_line:shell_entry_point']
      },
      zip_safe=False)