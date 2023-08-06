<h1 align="center">Offstack App</h1>
<h3 align="center">Locally store <b>Stackoverflow</b> answers, comments, ratings and personal keywords of your favorite marked questions. <b>Only for Linux.</b></h3>

<div align="center">
  <a href="https://github.com/calexandru2018/offstack-app/releases/latest">
      <img alt="Build Status" src="https://img.shields.io/github/release/calexandru2018/offstack-app.svg?style=flat" />
  </a>
  <a href="https://pepy.tech/project/offstack-app">
    <img alt="Downloads" src="https://pepy.tech/badge/offstack-app">
  </a>   
    <a href="https://pepy.tech/project/offstack-app/week">
      <img alt="Downloads per Week" src="https://pepy.tech/badge/offstack-app/week">
    </a>
</div>
<div align="center">
  <a href="https://liberapay.com/calexandru2018/donate"><img alt="Donate using Liberapay" src="https://liberapay.com/assets/widgets/donate.svg"></a>
</div>
<div align="center">
  <img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/offstack-app?color=Yellow&label=python&logo=Python&logoColor=Yellow">
</div>
<div align="center">
  <a href="https://www.codefactor.io/repository/github/calexandru2018/offstack-app">
    <img src="https://www.codefactor.io/repository/github/calexandru2018/offstack-app/badge" alt="CodeFactor" />
  </a>
  <a href="https://github.com/calexandru2018/offstack-app/blob/master/LICENSE">
    <img src="https://img.shields.io/pypi/l/offstack-app?style=flat" alt="License"></img>
  </a>
</div>
<div align="center">
    <a href="https://actions-badge.atrox.dev/calexandru2018/offstack-app/goto?ref=master">
        <img alt="GitHub Workflow Status (branch)" src="https://img.shields.io/github/workflow/status/calexandru2018/offstack-app/master flake8/master?label=master%20flake8">
    </a>
    <a href="https://actions-badge.atrox.dev/calexandru2018/offstack-app/goto?ref=testing">
      <img alt="GitHub Workflow Status (Testing)" src="https://img.shields.io/github/workflow/status/calexandru2018/offstack-app/testing flake8/testing?label=testing%20flake8">
    </a> 
</div>
<br/>
<p>
The main goal with <b>Offstack</b> is to make sure that developpers have access to their favorite stackoverflow questions&answers locally on their computers, without the need of using a browser and searching for previously saved issues.
</p>

### Installing Dependencies

**Dependencies:**

- python3.5+
- pip for python3 (pip3)
- setuptools for python3 (python3-setuptools)
- requests-oauthlib
- requests
- oauthlib
- selenium
- <a href="https://github.com/mozilla/geckodriver/releases">geckodriver</a>


Install the following packages based on your distro:

| **Distro**                              | **Command**                                                                                                                           |
|:----------------------------------------|:---------------------------------------------------------------------------------------------------------                             |
|Fedora/CentOS/RHEL                       | `sudo dnf install -y python3-gobject gtk3`                                              |
|Ubuntu/Linux Mint/Debian and derivatives | `sudo apt install -y python3-gi python3-gi-cairo gir1.2-gtk-3.0`                        |
|OpenSUSE/SLES                            | `sudo zypper install python3-gobject python3-gobject-Gdk typelib-1_0-Gtk-3_0 libgtk-3-0`  |
|Arch Linux/Manjaro                       | `sudo pacman -S python-gobject gtk3`       |


## Installing offstack

Before proceeding with with the next installation steps, make sure that you have downloaded <a href="https://github.com/mozilla/geckodriver/releases">geckodriver</a> and moved it into `/usr/lib` or `/usr/local/lib`, otherwise this will not work.

You can either install via <b>PIP</b> or by cloning the repository.

*Note: Make sure to run pip with sudo*

`sudo pip3 install offstack`

### To update to a new version

`pip3 install offstack --upgrade`

## Manual Installation

1. Clone this repository

    `git clone https://github.com/calexandru2018/offstack`

2. Step into the directory

   `cd offstack`

3. Install

    `python3 setup.py install`

### How to use

 `offstack`

### Not yet implemented:
- GUI
- Add own (personal) keywords
- Searching/Filter

## GUI Layout

<p align="center">
  <img src="https://i.imgur.com/P2D5mKE.png" alt="Advanced Settings"></img>
</p> 

<p align="center">
  <img src="https://i.imgur.com/BxJ2Fys.png" alt="Diagnosis Tool"></img>
</p> 