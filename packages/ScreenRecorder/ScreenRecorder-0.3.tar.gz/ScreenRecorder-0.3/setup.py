from setuptools import setup


setup(
    name='ScreenRecorder',
    version='0.3',
    author='foo',
    author_email='foo@foo.com',
    url='https://pypi.org/project/ScreenRecorder',
    description='A screen recorder.',
    install_requires=["keyboard", "moviepy", "pyaudio", "pyautogui", "pygame"],
    python_requires='>=3.6',
    py_modules=['ScreenRecorder'],)
