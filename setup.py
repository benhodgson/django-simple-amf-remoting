from distutils.core import setup

setup(
    name='django-simple-amf-remoting',
    version='0.1.0b',
    license='Public Domain',
    description='A simplified API for AmFast\'s AMF remoting functionality, '
        'designed to make Django AMF remoting simple and painless.',
    package_dir = {'':'src'},
    py_modules=['django_amf_remoting'],
    url='http://github.com/benhodgson/django-simple-amf-remoting',
    author='Ben Hodgson',
    author_email='ben@benhodgson.com',
    keywords = ['django', 'amf', 'amf0', 'amf3', 'flash', 'remoteobject',
        'rpc', 'remoting', 'pyamf', 'amfast'],
    classifiers = [
        'Programming Language :: Python',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Framework :: Django',
        'License :: Public Domain',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
