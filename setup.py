from setuptools import setup, Extension

module = Extension(
    'msp3520',  # モジュール名を msp3520 に変更
    sources=['msp3520/msp3520.c'],
    extra_compile_args=['-O3'],  # 最適化オプション
)

setup(
    name='msp3520',
    version='0.1',
    description='A library for displaying text on the MSP3520 display.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    ext_modules=[module],
    packages=['msp3520'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: C',
        'Operating System :: OS Independent',
    ],
)

