from distutils.core import setup
setup(
  name = 'BadCustomerDetector',         
  packages = ['BadCustomerDetector'],   
  version = '0.1',      
  license='MIT', 
  description = 'Test Detector For Auckland Transsport',   # Give a short description about your library
  author = 'Sunny Long',                   # Type in your name
  author_email = 'sunnyly2016@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/sunnyly2016/BadCustomerDetector',   # Provide either the link to your github or to your website
  download_url = '',    # I explain this later on
  keywords = ['AT', 'Data Science', 'Fraud'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'pandas',
          'numpy',
          'sklearn',
          'kneed',
          'scipy',
          'pyod'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',  
    'Intended Audience :: Developers',      
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8'
  ],
)
