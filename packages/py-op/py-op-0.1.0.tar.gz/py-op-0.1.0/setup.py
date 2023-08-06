from setuptools import setup, find_packages

setup(
    name='py-op',
    version='0.1.0',
    description = 'Python operators for easier chaining',
    author='Yilun Guan',
    author_email='zoom.aaron@gmail.com',
    packages=find_packages(include=['pyop']),
    install_requires=['fn','toolz'],
    license='MIT',
    url = 'https://github.com/guanyilun/pyop',
    download_url = 'https://github.com/guanyilun/pyop/archive/v0.1.0.tar.gz',
    keywords = ['functional programming', 'operator', 'utility'],
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
