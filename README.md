#PITCH

## Description
#### This is a web application that allows users to express themselves using a pitch. They can choose which category to write a pitch in and can view and comment on other user pitches.
#### By **Steve Kimanthi**
The user can:
* See various pitches, starting with the most recent
* Comment on pitches that they like
* Upvote pitches
* Downvote pitches
* Submit new pitches
## Setup/Installation Requirements
### Prerequisites
* python3.6
* pip
* Virtual environment(virtualenv)

### Cloning and running
* Clone the application using git clone(this copies the app onto your device). In terminal:

          $ git clone https://github.com/Vohsty/Pitch.git
          $ cd pitch

* Creating the virtual environment

          $ python3.6 -m venv --without-pip virtual
          $ source virtual/bin/env
          $ curl https://bootstrap.pypa.io/get-pip.py | python

* Installing Flask and other Modules

          $ python3.6 -m pip install Flask
          $ python3.6 -m pip install Flask-Bootstrap
          $ python3.6 -m pip install Flask-Script

* Run the application:

          $ chmod a+x start.sh
          $ ./start.sh
### Testing the Application
* To run the tests for the class files:

          $ python3.6 manage.py test

## Technologies Used
* Python 3.6
* Flask
## Behaviour driven development/ Specifications

| Behaviour |  Sample Input | Sample Output |
| :---------------- | :---------------: | :------------------ |
| View Categories | Click on category | List of categories is displayed |
| Add new pitch | Submit New Pitch | Authentication page is displayed and users can add new pitches|
| Add Comment | Click on Comment | Form where user can fill in is displayed after login|
| Upvote pitch | Click on Upvote| Current pitch get +1 upvote|
| Downvote pitch | Click on Downvote | Current pitch gets +1 downvote|

## Support and contact details
For any questions, troubleshooting or contributions,  find me on:
* Mobile: +254710998712
* Email: vohsty@gmail.com
### License
MIT License
Copyright (c) {2019} **Steve Kimanthi**
