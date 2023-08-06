from distutils.core import setup
setup(
  name = 'translingual',         
  packages = ['translingual'],   
  version = '0.13.1',      
  license='MIT',       
  description = 'Quick translation package using Google translate',   
  author = 'YohannesDatasci',
  author_email='yohannesdatasci2@gmail.com',                  
  keywords = ['translate', 'multi-thread'],   
  install_requires=[            
          'nltk',
          'selenium',
          'geckodriver_autoinstaller'
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
  ],
)