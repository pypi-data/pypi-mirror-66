import setuptools.command.install
import shutil
from distutils.sysconfig import get_python_lib


class CompiledLibInstall(setuptools.command.install.install):
    """
    Specialized install to install to python libs
    """

    def run(self):
        """
        Run method called by setup
        :return:
        """
        # Get filenames from CMake variable
        filenames = '/OpenDB/build/src/swig/python/opendbpy.py;/OpenDB/build/src/swig/python/_opendbpy.so'.split(';')

        # Directory to install to
        install_dir = get_python_lib()

        # Install files
        [shutil.copy(filename, install_dir) for filename in filenames]


if __name__ == '__main__':
    setuptools.setup(
        name='opendbpy',
        version='0.0.2',
        packages=setuptools.find_packages(),
        license='BSD-3 License',
        description = 'Database and Tool Framework for EDA',
        author='Abdelrahman Hosny',
        author_email='abdelrahman_hosny@brown.edu',
        url = 'https://github.com/EDAAC/ICTuner',
        download_url = 'https://github.com/EDAAC/ICTuner/archive/v_0.0.2.tar.gz',
        keywords = ['EDA', 'Electronic', 'Design', 'Automation', 'Parameter', 'Tuning', 'Search', 'Exploration'],
        install_requires=[],
        classifiers=[
            'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
            'Intended Audience :: Developers',
            'Topic :: Scientific/Engineering :: Electronic Design Automation (EDA)',
            'License :: OSI Approved :: BSD License',
            'Programming Language :: Python :: 3',
            'Operating System :: POSIX :: Other'
        ],
        package_data={'opendbpy': ['opendbpy.py', '_opendbpy.so']},
        long_description = 'Database and Tool Framework for EDA',
        long_description_content_type = 'text/markdown',

    )
