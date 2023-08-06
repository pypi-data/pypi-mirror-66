from distutils.core import setup
setup(
  name = 'tkCharacter',
  packages = ['tkCharacter'],
  version = '0.1',
  license='MIT',
  description = 'Allows for effortless creation of playable and AI 2d characters in python games',
  author = 'Don Charles - Lambert',
  author_email = 'your.email@domain.com',
  url = 'https://github.com/DonCharlesLambert/tkCharacter',
  download_url = 'https://github.com/DonCharlesLambert/tkCharacter/archive/0.1.tar.gz',    # I explain this later on
  keywords = ['tkinter', 'games', 'characters'],
  install_requires=[            # I get to this in a second
          'tkinter',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
  ],
)