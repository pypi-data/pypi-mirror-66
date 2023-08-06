from distutils.core import setup

with open("README") as f:
    long_description = f.read()

setup(name='easypwd',
      version='0.3.7',
      description='easy password generate libary.',
      author='L34Rn',    
      author_email='security@xatu.edu.cn',
      py_modules=['easypwd'],
      scripts=['Scripts/easypwd.bat', 'Scripts/easypwd.py'],
      platforms=['Windows'],
      License='GPL',
      data_files=[('README', ['README']), ('LICENSE', ['LICENSE'])],
      long_description=long_description,
      url='http://security.xatu.edu.cn',
      download_url='https://pypi.org/project/easypwd/',
      python_requires='>=2.6, <3.0',
)