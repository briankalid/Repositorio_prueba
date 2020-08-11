# Instructions
## Installation and use.
### Install requirements
#### REquiere requires python 3(tested on python 3.8)
- Open a terminal.
  - 1. Write: sudo apt-get install python-dev default-libmysqlclient-dev libssl-dev or pacman -S base-devel(if you use arch).
  - 2. Write: pip3 install twitter.
  - 3. Write: pip3 install tweepy.
  - 4. Write: pip3 install flask.
  - 5. Write: pip3 install flask_mysqldb.
  - 6. Write: pip3 install numpy
  - 7. Write: pip3 install pandas.
  - 8. Write: pip3 install matplotlib
  - 9. Write: sudo apt-get install nano.
- Download this [project](trend_tweet.py).
### Use
- Open a terminal into folder project.
  - 1. Write: nano secret.py.
  - 2. Insert your keys inside.
  - 2. Write: nano db.json.
  - 2. Insert your database keys inside.
  - 3. Save and close.
  #### To update data and create graphics:
    - 1. Write: python main.py.
  #### To deploy web service in localhost:
    - 1. Write: python web.py
