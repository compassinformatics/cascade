Recursion
=========

This page contains notes on the use of recursion in the cascade library, and on Python in general. These were written
when using Python 2.7 so may no longer be applicable. 


+ Longest path in the country is 159 segments (01_951 to 01_7100)
+ Python maximum recursion limit is 1000 (a conservative value)
+ No tail call optimisation. See http://neopythonic.blogspot.pt/2009/04/tail-recursion-elimination.html

  From Guido van Rossum:

    TRE is incompatible with nice stack traces: when a tail recursion is eliminated, 
    there's no stack frame left to use to print a traceback when something goes wrong later
    the idea that TRE is merely an optimization, which each Python implementation can choose to implement or not, is wrong. Once tail recursion elimination exists, 
    developers will start writing code that depends on it, and their code won't run on implementations that don't provide it

+ Python prevents the interpreter stack from growing larger than ``sys.getrecursionlimit()``. When you hit that limit you get
  ``Fatal Python error: Cannot recover from stack overflow.``

  You can cause a 'real' stack overflow if you call sys.setrecursionlimit(N) with a value of N larger than your system can 
  actually handle and then try to recurse to that depth. At some point your system will run out of stack space 
  and the Python interpreter will crash.

+ If the exercise is intended to be recursion-based, a tail-call optimized language, like a lisp/Scheme
+ Program allocated a stack - set amount of memory limited to RAM - other applications. 

  When a program attempts to use more space than is available on the call stack (that is, when it attempts to access memory 
  beyond the call stack's bounds, which is essentially a buffer overflow), the stack is said to overflow, 
  typically resulting in a program crash

+ http://deeplearning.net/software/theano/tutorial/python-memory-management.html

  Freeing memory - in general you can't. Even if you remove all the references to an object, it is left to the python 
  implementation to re-use or free the memory.
  Approach based on scientific paper.
