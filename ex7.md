Lazy evaluation
---------------
Lazy evaluation delays the computation of values until they are needed. 
In Python, this is often done using generators, 
which yield values one at a time rather than computing all at once.

Eager evaluation computes all values immediately, even if they are not needed right away
for example - list() (without a generator).

Lazy evaluation is more efficient in terms of memory and performance 
when not all values are required upfront.

In the program:
---------------
Eager evaluation:
Using "list(generate_values())" generates all values upfront and then go over all of them 
in the second time to processes the [square(x) for x in values].

Lazy evaluation:  
Using squared_values = "[square(x) for x in generate_values()]"
only generates each value when it's needed for squaring.
The list comprehension [square(x) for x in generate_values()] lazily pulls values from the generator one at a time as needed by square(x). Each value is generated, squared, and then the next value is requested, avoiding upfront computation and memory consumption.
