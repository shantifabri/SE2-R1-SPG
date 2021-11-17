# SE2-R1-SPG
Second project for Software Enineering II at PoliTo, group R1

----------

#### How to run with docker?

Firstly, you should clone our project locally, and then switch to the project directory, cd to project directory and execute the following command: `'docker build -t se2r1/spg:v1 .'`

Waiting for the process of pulling the images, after finished, use `'docker images'`, you will find the image named se2r1/spg which you build before. Now execute `'docker run -p 41999:5000 se2r1/spg:v1'`in your bash to run, and then you can visit http://127.0.0.1:41999/ to explore our project.

----------

** Disclaimer, the layout of the project, inizialization and tests are greatly based on [this](https://gitlab.com/patkennedy79/flask_user_management_example) repository by Patrick Kennedy.