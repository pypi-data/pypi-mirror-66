from setuptools import setup,find_packages
setup(name='takagiabm',
      version='0.2.3',
      description='python abm(Agent Based Model) framework like netlogo/mesa,  based on numpy,pyopengl and pyqt5.',
      url='https://gitee.com/hzy15610046011/TakagiABM',
      author='Zhanyi Hou',
      author_email='3120388018@qq.com',
      license='MuLan2.0',
      packages=find_packages(),
      include_package_data = True

      )#package_data={'':['hat.png']})
     # zip_safe=False,install_requires = ['pyqt5','pyqtgraph','numpy','pyopengl'])
