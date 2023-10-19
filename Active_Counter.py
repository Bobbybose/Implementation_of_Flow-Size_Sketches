import random

# Class for an Active Counter
# Half of bits are for number, other half for exponent
class ActiveCounter:
    # Class initialization takes in size of the active counter
    def __init__(self, num_bits):
        # Number and exponent part of counter
        self.n = 0
        self.e = 0
        
        # Size of counter
        self.num_bits = num_bits
    # init()

    # Givens: Amount to increment
    # Returns: None
    # Description: Probabilistic increment of the counter a given number of times
    def increment(self, amount):
        # Attempt to increment a given number of times
        for i in range(amount):
            # If the random probability check succeeds
            if 1/(2**self.e) > random.uniform(0, 1):
                # Increment number
                self.n += amount

                # If number part of counter exceeds bit size
                if self.n >= 2**(self.num_bits/2)-1:
                    # Increment exponent
                    self.e += 1
                    # Right shift counter
                    self.n = int(self.n/2)
        # increment()

# ActiveCounter


def main():
    # Creating a 32-bit active counter
    counter = ActiveCounter(32)

    # Incrementing by 1 1,000,000 times
    for num in range(1000000):
        counter.increment(1)

    # Checking and printing final value of counter
    final_value = counter.n * 2**counter.e
    print("Final value: " + str(final_value))
# main()


main()