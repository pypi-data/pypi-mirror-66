from setuptools import setup


def read_readme():
    with open("README.md", 'r') as file:
        return file.read()


def read_requirements():
    with open("requirements.txt", 'r') as file:
        return file.read().split('\n')


setup(
    name='flamma',
    version='0.1',
    description='\"FLAMMA gcode laser tools\" is a comprehensive suite of opensource laser cutting and engraving extensions for Inkscape >= 1.0',
    long_description=read_readme(),
    url='https://github.com/PadLex/FLAMMA-gcode-laser-tools',
    author='Alexander Padula',
    author_email='amberscript.contact@gmail.com',
    license='MIT',
    packages=['flamma'],
    install_requires=read_requirements(),
    entry_points={
        'console_scripts': ['open_gui=flamma.menu:open_gui'],
    },
    zip_safe=False
)
