# setup.py is required to build our application as a package. When we do pip install something it internally runs setup.py
#find_packages works by finding __init__.py files in our src directories
#Each folder with __init__.py behaves as a package that find_packages will identify
from setuptools import find_packages, setup
from typing import List

HYPHEN_E_DOT='-e .'

def get_requirements(file_path:str) -> List[str]:
    '''
    This function returns list of requirements from requirements.txt
    '''
    requirements=[]
    with open(file_path) as file_obj:   #reading requirements.txt
        requirements=file_obj.readlines()   #reads \n also
        requirements=[req.replace("\n", "") for req in requirements]
        if HYPHEN_E_DOT in requirements:
            requirements.remove(HYPHEN_E_DOT)
    
    return requirements
    


setup(
    name='mlproject',
    version='0.0.1',
    author='aman',
    author_email='amanrehman18@gmail.com',
    packages=find_packages(),
    #install_requires=['pandas', 'numpy', 'seaborn']     #Automatically install these libraries
    install_requires=get_requirements('requirements.txt') #We may need to install many dependencies we dont want to manually write all.
)