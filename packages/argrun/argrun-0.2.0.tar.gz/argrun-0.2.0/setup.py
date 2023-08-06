from distutils.core import setup
setup(
  name = 'argrun',
  packages = ['argrun'], 
  version = '0.2.0',  
  license='MIT', 
  description = 'a small library that wraps argparse to map arguments to decorated functions',
  author = 'nilput',                  
  author_email = 'nilputs@gmail.com',   
  url = 'https://github.com/nilput/argrun/',  
  download_url = 'https://github.com/nilput/argrun/releases/download/v0.2/argrun-0.2.tar.gz', 
  keywords = ['argparse', 'arguments', 'cli'],
  install_requires=[        
          'argparse',
      ],
  classifiers=[
    'Development Status :: 4 - Beta',     
    'Intended Audience :: Developers',    
    'Topic :: Software Development',
    'License :: OSI Approved :: MIT License',
    'Environment :: Console',  
    'Programming Language :: Python :: 3',     
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
  ],
)
