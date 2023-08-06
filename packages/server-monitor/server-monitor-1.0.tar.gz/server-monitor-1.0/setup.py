from distutils.core import setup
setup(
  name = 'server-monitor',         # How you named your package folder (MyLib)
  packages = ['server-monitor'],   # Chose the same as "name"
  version = '1.0',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'This is a package utilising psutil to give system stats for a telegram bot',   # Give a short description about your library
  author = 'Abhishek Kushwaha',                   # Type in your name
  author_email = 'thecrazycoderabhi@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/abhishekkushwaha4u/Client_Coder_for_VM_Server_Monitor',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/abhishekkushwaha4u/Client_Coder_for_VM_Server_Monitor/archive/v_1.0.tar.gz',    # I explain this later on
  keywords = ['Telegram', 'Server Monitor', 'Bot'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'asgiref==3.2.7'
          'certifi==2020.4.5.1'
          'chardet==3.0.4'
          'Django==3.0.5'
          'djangorestframework==3.11.0'
          'idna==2.9'
          'psutil==5.7.0'
          'python-crontab==2.4.1'
          'python-dateutil==2.8.1'
          'pytz==2019.3'
          'requests==2.23.0'
          'six==1.14.0'
          'sqlparse==0.3.1'
          'urllib3==1.25.8'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)