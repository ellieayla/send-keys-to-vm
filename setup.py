from setuptools import setup

setup(
    name='send-keys-to-vm',
    version='1.0',
    py_modules=["send_keys_to_vm"],
    install_requires=['pyVmomi>=6.5'],
    license="Apache Software License 2.0",
    url='',
    author='Alan J Castonguay',
    author_email='alan@verselogic.net',
    description='Send USB Scancodes to a VMware vSphere Virtual Machine',
    classifiers=[
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Development Status :: 4 - Beta',
        'Natural Language :: English',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
