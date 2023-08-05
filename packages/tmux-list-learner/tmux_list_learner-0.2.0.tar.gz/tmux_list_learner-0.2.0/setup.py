from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='tmux_list_learner',
    version='0.2.0',
    description='List learning tool using tmux windows',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/flaxandteal/tmux_list_learner',
    author='Phil Weir',
    author_email='phil.weir@flaxandteal.co.uk',
    license='MIT',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7'
    ],
    keywords='tmux learning',
    install_requires=[
        'Click',
        'pyyaml',
        'appdirs'
    ],
    entry_points='''
        [console_scripts]
        tmux-list-learner=tmux_list_learner.scripts.tmux_list_learner:cli
    '''
)
