from setuptools import setup  # , find_packages

# Clasificadores: https://pypi.org/pypi?%3Aaction=list_classifiers


def get_readme():
    readme_txt = ""
    try:
        readme_txt = open('README.md').read()
    except Exception as e:
        print("Ha ocurrido un inconveniente: " + str(e))
    return readme_txt


setup(
    name='pyanna',
    version='0.1.0',
    author='Ecom Developers',
    author_email='simono@ecom.com.ar',
    description=('Especificaciones Plataforma AnnA'),
    long_description=get_readme(),
    license='BSD',
    keywords='3des',
    url='https://bitbucket.org/lucasecom/especificaciones_simono/src/master/',
    packages=['pyanna', 'pyanna.cipher'],
    # packages=find_packages(),
    package_data={
        # 'starwars_ipsum': ['*.txt']
    },
    install_requires=['pycryptodome==3.9.7', 'pyDes==2.0.1'],
    classifiers=[
        'Development Status :: 1 - Planning',
        'License :: OSI Approved :: GNU Lesser General Public License v2 (LGPLv2)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Topic :: Utilities',
    ]
)
