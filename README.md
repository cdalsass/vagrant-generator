# Using vagrant-generator.py

In order to use vagrant-generator.py, you must first use have python 2.7 on your system (don't install Python 3!)

Once python is installed, you will need pip, and then you will need to install the requirements from the requirements.txt file.

On Windows:

```
python get-pip.py
pip install -r requirements.txt
```

On Mac/Linux:

```
sudo easy_install pip
pip install -r requirements.txt
```

you can then execute the script with:

```
python vagrant-generator.py -h
```

to display all the current options.

# Generating a new site/app

Copy files into your local site folder, modifying the env-local.yml and bootstrap.tpl to match your target environment.

```
cp Vagrantfile bootstrap.tpl env-local.yml [local site folder - keep out of public directories]
```

Generate your bootstrap.sh

```
python vagrant-generator.py --environment=local --render
```
Vagrant up!

```
vagrant up
```
