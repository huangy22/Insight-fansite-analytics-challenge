# Table of Contents
1. [Challenge Summary](README.md#challenge-summary)
2. [Details of Features](README.md#details-of-implementation)
3. [Description of Data](README.md#description-of-data)
4. [Code Dependencies and Structure](README.md#code-dependencies-and-structure)
5. [Repo directory structure](README.md#repo-directory-structure)


## Challenge Summary

This project is designed for a NASA fan website that generates a large amount of Internet traffic data.  The code allows the user to perform basic analytics on the server log file, provide useful metrics, and implement basic security measures. 

The features are described below: 

### Feature 1: 
List the top 10 most active host/IP addresses that have accessed the site.

### Feature 2: 
Identify the 10 resources that consume the most bandwidth on the site.

### Feature 3:
List the top 10 busiest (or most frequently visited) 60-minute periods. 

### Feature 4: 
Detect patterns of three failed login attempts from the same IP address over 20 seconds so that all further attempts to the site can be blocked for 5 minutes. Log those possible security breaches.

### Feature 5:
In Feature 3, the provided 60-minute periods  are allowed to overlap with each other, which results in the top 10 periods being very similar and having big overlaps. In this feature, the selected top 10 busiest periods are not allowed to overlap, which turns out to be more informative than feature 3.

### Further Features:
This dataset is inspired by real NASA web traffic, which is very similar to server logs from e-commerce and other sites. Monitoring web traffic and providing these analytics is a real business need, but it’s not the only thing you can do with the data. Feel free to implement additional features that you think might be useful.

## Details of Implementation

### Feature 1 
List in descending order the top 10 most active hosts/IP addresses that have accessed the site.

**Output**: The 10 most active hosts/IP addresses in descending order and how many times they have accessed are written in a file named `hosts.txt`. There are at most 10 lines in the file, and each line includes the host (or IP address) followed by a comma and then the number of times it accessed the site. 

e.g., `hosts.txt`:

    example.host.com,1000000
    another.example.net,800000
    31.41.59.26,600000
    …

### Feature 2 
Identify the top 10 resources on the site that consume the most bandwidth. Bandwidth consumption is estimated from bytes sent over the network and the frequency by which they were accessed.

**Output**: These most bandwidth-intensive resources, sorted in descending order and separated by a new line, are written to a file called `resources.txt`. The file contains at most 10 lines with each line containing the resource.

e.g., `resources.txt`:
    
    /images/USA-logosmall.gif
    /shuttle/resources/orbiters/discovery.html
    /shuttle/countdown/count.html
    …


### Feature 3 
List in descending order the site’s 10 busiest (i.e. most frequently visited) 60-minute period. The 60-minute periods are allowed to overlap.

**Output**: The start time of each 60-minute window followed by the number of times the site was accessed during that time period are written to a file named `hours.txt`.  The file contains at most 10 lines with each line containing the start of each 60-minute window, followed by a comma and then the number of times the site was accessed during those 60 minutes. The 10 lines are listed in descending order with the busiest 60-minute window shown first. 

e.g., `hours.txt`:

    01/Jul/1995:00:00:01 -0400,100
    01/Jul/1995:00:00:10 -0400,22
    05/Jul/1995:09:05:02 -0400,10
    01/Jul/1995:12:30:05 -0400,8
    …

### Feature 4 
Detect patterns of three consecutive failed login attempts over 20 seconds in order to block all further attempts to reach the site from the same IP address for the next 5 minutes. Each attempt that would have been blocked is written to a log file named `blocked.txt`.

**Output**:
e.g., `blocked.txt`

    uplherc.upl.com - - [01/Aug/1995:00:00:07 -0400] "GET / HTTP/1.0" 304 0
    uplherc.upl.com - - [01/Aug/1995:00:00:08 -0400] "GET /images/ksclogo-medium.gif HTTP/1.0" 304 0
    …

**Details of the feature**: If an IP address has not reached three failed login attempts during the 20 second window, a login attempt that succeeds during that time period will resets the failed login counter and 20-second clock. The next failed login attempt will be counted as 1, and the 20-second timer would begin there. In other words, this feature should only be triggered if an IP has  3 failed logins in a row, within a 20-second window.

The following illustration shows how this feature works, and when three failed login attempts would trigger 5 minutes of blocking:

![Feature 4 illustration](images/feature4.png)

Note that this feature is independent with the other features in this code. For instance, any requests that end up in the `blocked.txt` file will still be counted toward the most active IP host calculation, bandwidth consumption and busiest 60-minute period.

### Feature 5 
List in descending order the site’s 10 busiest (i.e. most frequently visited) 60-minute period while enforcing the requirement that the time windows don't overlap. The provided results are the 10 best possible periods without overlapping.

**Output**: The start time of each 60-minute window followed by the number of times the site was accessed during that time period are written to a file named `hours_no_overlap.txt`. The file contains at most 10 lines with each line containing the start of each 60-minute window, followed by a comma and then the number of times the site was accessed during those 60 minutes. The 10 lines are listed in descending order with the busiest 60-minute window shown first. 

e.g., `hours_no_overlap.txt`:
 
    01/Jul/1995:00:00:01 -0400,100
    02/Jul/1995:10:00:07 -0400,22
    05/Jul/1995:09:05:02 -0400,10
    01/Jul/1995:12:30:05 -0400,8
    …

### Additional Features

Feel free to implement additional features that might be useful to derive further metrics or prevent harmful activity. These features will be considered as bonus while evaluating your submission. If you choose to add extras please document them in your README and make sure that they don't interfere with the above four (e.g. don't alter the output of the four core features).


## Description of Data

The data can be downloaded here: https://drive.google.com/file/d/0B7-XWjN4ezogbUh6bUl1cV82Tnc/view

The input file, named as `log.txt`, is in ASCII format with one line per request, containing the following columns:

* **host** making the request. A hostname when possible, otherwise the Internet address if the name could not be looked up.

* **timestamp** in the format `[DD/MON/YYYY:HH:MM:SS -0400]`, where DD is the day of the month, MON is the abbreviated name of the month, YYYY is the year, HH:MM:SS is the time of day using a 24-hour clock. The timezone is -0400.

* **request** given in quotes.

* **HTTP reply code**

* **bytes** in the reply. Some lines in the log file will list `-` in the bytes field. For the purposes of this challenge, that is interpreted as 0 bytes.

e.g., `log.txt`

    in24.inetnebr.com - - [01/Aug/1995:00:00:01 -0400] "GET /shuttle/missions/sts-68/news/sts-68-mcc-05.txt HTTP/1.0" 200 1839
    208.271.69.50 - - [01/Aug/1995:00:00:02 -400] “POST /login HTTP/1.0” 401 1420
    208.271.69.50 - - [01/Aug/1995:00:00:04 -400] “POST /login HTTP/1.0” 200 1420
    uplherc.upl.com - - [01/Aug/1995:00:00:07 -0400] "GET / HTTP/1.0" 304 0
    uplherc.upl.com - - [01/Aug/1995:00:00:08 -0400] "GET /images/ksclogo-medium.gif HTTP/1.0" 304 0
    ...

## Code Dependencies and Structure

If your solution requires additional libraries, environments, or dependencies, you must specify these in your `README` documentation. See the figure below for the required structure of the top-most directory in your repo, or simply clone this repo.

## Repo directory structure


    ├── README.md 
    ├── run.sh
    ├── run_test.sh
    ├── src
    │   └── process_log.py
    ├── log_input
    │   └── log.txt
    ├── log_output
    |   └── hosts.txt
    |   └── hours.txt
    |   └── hours_no_overlap.txt
    |   └── resources.txt
    |   └── blocked.txt
    ├── insight_testsuite
        └── run_tests.sh
        └── tests
            └── test_features
            |   ├── log_input
            |   │   └── log.txt
            |   |__ log_output
            |   │   └── hosts.txt
            |   │   └── hours.txt
            |   │   └── resources.txt
            |   │   └── blocked.txt
            ├── mytest
                ├── log_input
                │   └── log.txt
                |__ log_output
                    └── hosts.txt
                    └── hours.txt
                    └── resources.txt
                    └── blocked.txt