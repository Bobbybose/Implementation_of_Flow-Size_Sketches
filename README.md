# CS685 - Internet Data Streaming 
# Project 3 - Implementation of Flow-Size Sketches
**Author:** Bobby Bose

## Description
- This is an implementation of a CountMin, Counter Sketch, and Active Counter
- There are three Python scripts, one for each counter
- An example output is given in three output (.out) files
- Hash function used in all code was based off of the folding method from https://www.herevego.com/hashing-python/

## Required Packages and Modules
- No external packages required 
- The only required modules are the sys, and random modules built into Python

## CountMin
- To run, do 'python ./CountMin.py input_file num_counter_arrays num_counter_per_array'
- **Architecture Operation:**
    - Consists of a given number of counter arrays, each with a given number of counters
    - Counters increment to reflect flow size (number instances of flow)
    - Each flow is hashed to one counter in each array
    - When querying, choose smallest count (least error)
        - Error is difference between actual and estimated count
- **Program Flow**
    - Read in an input file with flow ids and their size
    - Records the size of all flows in CountMin
    - Query for estimated size of all flows and compute average error of all flows
- **Output:**
    - First line is the average error among all flows
    - Next 100 lines are the flows with the largest estimated size

## Counter Sketch
- To run, do 'python ./Counter_Sketch.py input_file num_counter_arrays num_counter_per_array'
- **Architecture Operation:**
    - Consists of a given number of counter arrays, each with a given number of counters
    - Counters reflect flow size (number instances of flow)
    - Each flow is hashed to one counter in each array
        - Each flow is also hashed with a separate hash function
            - If the last bit of the binary form of the hash value is 1, then the counter the flow hashes to increments by the size
            - If the last bit is 0, then the counter decrements by the size instead
    - When querying, choose medium count
        - Need to convert negative numbers if binary hash resulted in decrementing
- **Program Flow**
    - Read in an input file with flow ids and their size
    - Records the size of all flows in CountMin
    - Query for estimated size of all flows and compute average error of all flows
- **Output:**
    - First line is the average error among all flows
    - Next 100 lines are the flows with the largest estimated size


## Active Counter
- To run, do 'python ./Active_Counter'
- **Architecture Operation:**
    - Active Counter is a given number of bits in size
    - Half of counter is number part (n)
    - Half of counter is exponent part (e)
    - Counter has probabilistic incrementing
        Probability to increment = 1/(2^e)
    - When counter increments, n increases by 1
        - If n overflows (n > 2^(counter_size/2)-1), then e increments by 1 and n right shifts (n /= 2)
- **Program Flow**
    - Active Counter created of size 32 bits
    - Counter increments by 1 1,000,000 times
- **Output:**
    - Final value stored in counter

