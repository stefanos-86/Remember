# Remember
What? GDB has a Python interpreter inside?

Well, yes. A whole [Python API](https://sourceware.org/gdb/onlinedocs/gdb/Python-API.html#Python-API).

## What's to Remember?
This is another "try and see" experiment. The GDB script inside scans the memory saved in a core file to find pointers and objects inside. Anything that the core file "rememebers", hence the name. It gives a nice graph.

The above comes from:
```
...Remember$ python remember.py -o niceGraph.svg ./testCores/demo.3551 ./testPrograms/demo
```

It is in no way perfect and probably impossible to use on any "real" program. The code is not the best either. But it shows it can be done, and this is surprising enough to me!

To make this boondoggle work you need to be on Linux, with [gcc](https://gcc.gnu.org/) and GDB.

## What can't you Remeber?
Lots of things, but the most obvious limit is the automatic scanning of arrays. Says you have a int* pointer: just an int? Or an int in the middle of an array? There is no data in a core file to understand this is any reliable way.

Other cases have not been considered due to lack of time to waste on this project. Among the things I "forgot" to handle: arrays inside objects, arrays of pointers, multi dimensional arrays, lamda functions, smart pointer, STL... You can forget about them too - it is unlikely I'll find the time.

## The testing framework.
Where are the unit tests? Well, there aren't. Since I litteraly did not know what I was doing, I had an hard time predicting the output. What should the Graphiz input be to get the proper graph? What is GDB going to return me under a given situation? How am I going to prepare a test case or an assert() without knowing?

What you find instead is a set of test C++ programs and a couple of scripts to quickly create core dumps, run the tool on them and compare the resulting graph with a known good output. The programs have infinite loops inside so they "wait" at the right moment until `gcore` comes and dumps them. It is less automated testing and more automated tampering, but it gets the job done.

In practice:
```
.../Remember$ python CreateTestCores.py
<Lots of compiling goes on there - will ask your root password to core the programs>

.../Remember$ python FullStackTests.py
<Lots of output, whatch out for FAIL indications>
```
You can call the FullStackTests with the -t option to launch a single case.

## Special thanks
The GDB docs are incorrect. [Vincent saved the day](https://vjordan.info/log/fpga/tag/gdb.html)!
