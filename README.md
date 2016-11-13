# PollTrack
## Overview
PollTrack is a Twitterbot, written in Python, designed to track the polls during the 2016 presidential election.

Utilizing public state and national polling data from the [Huffington Post Pollster API](http://elections.huffingtonpost.com/pollster) and the [Twitter API](https://dev.twitter.com/overview/api), PollTrack collected and tweeted the latest polls using a dedicated Twitter account: [@PollTrackBot](https://twitter.com/PollTrackBot).

Additionally, PollTrack could be configured to calculate a 7-day rolling average of national and state polls, and tweet the results along with a plot at a desginated time daily. 

## Intallation and Use
**Note: PollTrack was designed to run using poll data released during the 2016 election season. The code was not designed to be run after the November 8 election.**

To install simply clone the repository into a desired directory:
`git clone https://github.com/haaspt/PollTrack.git`

### Setup

PollTrack requires the user to provide valid credentials for Twitter account, which is used to tweet new polls and graphs. To obtain credentials register a new app with Twitter's [Application Manager](https://apps.twitter.com/). Once registered, edit the `credentials.config.sample` file in the root directory using your prefered text editor and enter your access tokens and consumer keys. Once edited, save the file as `credentials.config`.

The user can configure which averages are calculated and when they are tweeted by editing the `plots.config` file.

PollTrack runs in a continuous loop, it is ideally hosted on a server, or a machine with uninterrupted internet access. To run PollTrack simply type:
`python main.py`

PollTrack can also be run in the background using the following command:
`sudo python main.py &`

### Required Dependencies
* [Pandas](http://pandas.pydata.org/)
* [Matplotlib](http://matplotlib.org/)
* [schedule](https://github.com/dbader/schedule)
* [python-twitter](https://github.com/bear/python-twitter)
