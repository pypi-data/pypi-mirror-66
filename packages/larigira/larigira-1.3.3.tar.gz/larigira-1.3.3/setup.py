import os
import sys

from setuptools import setup
from setuptools.command.test import test as TestCommand


def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as buf:
        return buf.read()


class PyTest(TestCommand):
    user_options = [("pytest-args=", "a", "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest

        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


setup(
    name="larigira",
    version="1.3.3",
    description="A radio automation based on MPD",
    long_description=read("README.rst"),
    long_description_content_type="text/x-rst",
    author="boyska",
    author_email="piuttosto@logorroici.org",
    license="AGPL",
    packages=["larigira", "larigira.dbadmin", "larigira.filters"],
    install_requires=[
        "Babel==2.6.0",
        "Flask-Babel==1.0.0",
        "pyxdg==0.26",
        "gevent==1.4.0",
        "flask-bootstrap",
        "python-mpd2",
        "wtforms==2.2.1",
        "Flask-WTF==0.14.2",
        "flask==0.11",
        "pytimeparse==1.1.8",
        "croniter==0.3.29",
        "werkzeug==0.14.1",
        "cachelib==0.1",
        "tinydb==3.12.2",
    ],
    tests_require=["pytest-timeout==1.0", "py>=1.4.29", "pytest==3.0"],
    python_requires=">=3.5",
    extras_require={"percentwait": ["mutagen"]},
    cmdclass={"test": PyTest},
    zip_safe=False,
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "larigira=larigira.larigira:main",
            "larigira-timegen=larigira.timegen:main",
            "larigira-audiogen=larigira.audiogen:main",
            "larigira-dbmanage=larigira.event_manage:main",
        ],
        "larigira.audiogenerators": [
            "mpd = larigira.audiogen_mpdrandom:generate_by_artist",
            "static = larigira.audiogen_static:generate",
            "http = larigira.audiogen_http:generate",
            "randomdir = larigira.audiogen_randomdir:generate",
            "mostrecent = larigira.audiogen_mostrecent:generate",
            "script = larigira.audiogen_script:generate",
        ],
        "larigira.timegenerators": [
            "frequency = larigira.timegen_every:FrequencyAlarm",
            "single = larigira.timegen_every:SingleAlarm",
            "cron = larigira.timegen_cron:CronAlarm",
        ],
        "larigira.timeform_create": [
            "single = larigira.timeform_base:SingleAlarmForm",
            "frequency = larigira.timeform_base:FrequencyAlarmForm",
            "cron = larigira.timeform_cron:CronAlarmForm",
        ],
        "larigira.timeform_receive": [
            "single = larigira.timeform_base:singlealarm_receive",
            "frequency = larigira.timeform_base:frequencyalarm_receive",
            "cron = larigira.timeform_cron:cronalarm_receive",
        ],
        "larigira.audioform_create": [
            "static = larigira.audioform_static:StaticAudioForm",
            "http = larigira.audioform_http:AudioForm",
            "script = larigira.audioform_script:ScriptAudioForm",
            "randomdir = larigira.audioform_randomdir:Form",
            "mostrecent = larigira.audioform_mostrecent:AudioForm",
        ],
        "larigira.audioform_receive": [
            "static = larigira.audioform_static:staticaudio_receive",
            "http = larigira.audioform_http:audio_receive",
            "script = larigira.audioform_script:scriptaudio_receive",
            "randomdir = larigira.audioform_randomdir:receive",
            "mostrecent = larigira.audioform_mostrecent:audio_receive",
        ],
        "larigira.eventfilter": [
            "maxwait = larigira.filters:maxwait",
            "percentwait = larigira.filters:percentwait",
        ],
    },
    classifiers=[
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Multimedia :: Sound/Audio",
    ],
)
