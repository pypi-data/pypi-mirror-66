cheesebread
===========

*cheesebread* is a data toolbox. In other words, it supports tools and shortcuts to 
get data from REST APIs into datasets without the hassle of explicitly handling 
every single step in the middle.

*cheesebread* handles:

  - data catalog and datasets
  - asynchronous communication to REST APIs
  - aggregate data into time series from REST APIs
  - authentication 
  - expiring tokens
  - request limits and retry on failure
  - deduplication

Rationale
^^^^^^^^^

More often than not, collectig data from REST APIs gets in the way of data analysis and  
machine learning. The toolbox implements a list of helpers that automate data collection. 

Moreover, when we are given aggregate data, for instance, an API endpoint that 
returns a user's number of interaction during a given period, the toolbox manages to create 
time series by asynchronously calling the API multiple times - a little bit hacky, but it wil get what we need. 

The toolbox is aimed to a somewhat incipient data science team whose main focus is to
get started with data analysis and not data collection. 

Versioning
^^^^^^^^^^

Always suggest a version bump. We use `Semantic Versioning <http://semver.org>`_.

Given a version number MAJOR.MINOR.PATCH, increment the:

- MAJOR version when you make incompatible API changes,
- MINOR version when you add functionality in a backwards-compatible manner, and
- PATCH version when you make backwards-compatible bug fixes.
