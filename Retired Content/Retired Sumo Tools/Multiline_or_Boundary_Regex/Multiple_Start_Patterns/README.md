This example shows how to specifcy boundary regex for multiple types of multiline messages that start with different patterns.

In the first 2 logs (see image) the start pattern is (a number string in brakcets, then an IP): 

- [10-19405] 65.152.122.170 - 

The third message starts with a timestamp :

- 2017-02-16 18:01:37,237 - 

See the IP_or_Timestamp regex for an example of boundary regex (option 1 | option 2)
