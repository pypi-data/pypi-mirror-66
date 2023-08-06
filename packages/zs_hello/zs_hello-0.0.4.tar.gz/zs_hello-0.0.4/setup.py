#from distutils.core import setup
from setuptools import setup, find_packages

VERSION = '0.0.4'

tests_require = []

install_requires = []

setup(name='zs_hello',
      url='https://github.com/zs527523251/hello',  # 项目包的地址
      author="zhousan",  # Pypi用户名称
      author_email='527523251@qq.com',  # Pypi用户的邮箱
      keywords='python pi',
      description='Automatically register models in the admin interface in a smart way.',
      license='MIT',  # 开源许可证类型
      classifiers=[
          'Operating System :: OS Independent',
          'Topic :: Software Development',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: Implementation :: PyPy'
      ],

      version=VERSION,
      install_requires=install_requires,
      tests_require=tests_require,
      test_suite='runtests.runtests',
      extras_require={'test': tests_require},

      entry_points={'nose.plugins': []},
      packages=find_packages(),
)
