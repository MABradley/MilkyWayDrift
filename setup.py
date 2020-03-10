from distutils.core import setup

setup(
    name='MilkywayDrift',
    version='0.1dev',
    packages=['milky_way_drift'],
    install_requires=[
        'kivy-deps.sdl2>=0.2.0',
        'kivy-deps.glew>=0.2.0',
        'Pillow>=7.0.0',
        'html5lib',
        'idna',
        'docutils>=0.16',
        'kivy>=1.11.1',
        'numpy>=1.18.1',
    ],
    license='MIT',
    long_description=open('README.md').read(),
)