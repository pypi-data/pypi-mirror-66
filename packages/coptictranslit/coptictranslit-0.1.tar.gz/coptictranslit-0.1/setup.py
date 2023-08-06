from setuptools import setup 
  
# reading long description from file 
with open('README.md') as file: 
    long_description = file.read() 
  
  
# specify requirements of your package here 
REQUIREMENTS = ['pynini'] 
  
# some more details 
CLASSIFIERS = [ 
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    'Operating System :: OS Independent',
    'Programming Language :: Python', 
    'Programming Language :: Python :: 2', 
    'Programming Language :: Python :: 2.6', 
    'Programming Language :: Python :: 2.7', 
    'Programming Language :: Python :: 3', 
    'Programming Language :: Python :: 3.3', 
    'Programming Language :: Python :: 3.4', 
    'Programming Language :: Python :: 3.5', 
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    ] 
  
# calling the setup function  
setup(name='coptictranslit', 
      version='0.1', 
      description='An inital release of a Coptic Transliterator', 
      long_description=long_description, 
      url='https://github.com/shehatamichael/coptic-transliteration', 
      author='Michael Shehata', 
      author_email='shehatamichael4@gmail.com', 
      packages=['translit'], 
      classifiers=CLASSIFIERS, 
      install_requires=REQUIREMENTS, 
      keywords='Coptic'
      ) 