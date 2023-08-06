from setuptools import setup



setup(
    name='fxpmath',
    version=__import__('fxpmath').__version__,
    author='francof2a',
    author_email='empty@empty.com',
    packages=['fxpmath'],
    description='A python library for fractional fixed-point arithmetic.',
    url='https://github.com/francof2a/fxpmath',
    download_url = 'https://github.com/francof2a/fxpmath.git',
    license='MIT',
    keywords=['fixed point', 'fractional', 'math', 'python', 'fxpmath', 'fxp'],
    install_requires=['numpy'],

    classifiers=[
        'Development Status :: 4 - Beta',
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Scientific/Engineering :: Physics",

    ]
)

