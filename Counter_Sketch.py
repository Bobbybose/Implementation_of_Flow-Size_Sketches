import sys
import random

def main():
    
    # Checking that the correct number of arguments was passed in
    if len(sys.argv) != 4:
        print("Invalid number of arguments")
        print("Program should be run in form 'python ./Counter_Sketch.py input_file num_counter_arrays num_counter_per_array'")
        return
    
    # Setting input parameters
    input_file = open(sys.argv[1], "r")
    num_counter_arrays = int(sys.argv[2])
    num_counters_per_array = int(sys.argv[3])
    
    # Creating counter arrays
    counter_arrays = []
    for i in range(num_counter_arrays):
        new_counter_array = [0] * num_counters_per_array
        counter_arrays.append(new_counter_array)

    # First line of input file is number of flows
    num_flows = int(input_file.readline())
    
    # Creating list for flows
    flows = [] 

    # Obtaining flows from input file
    for flow in range(num_flows):
        # Reading in a new line and extracting flow id and count
        curr_line = input_file.readline()
        flow_id = curr_line.split(' ')[0]
        curr_flow_count = int(curr_line.split(' ')[-1])

        flows.append((flow_id, curr_flow_count))

    
    # Creating hashes
    hashes = []
    for hash in range(num_counter_arrays):
        hashes.append(random.randrange(1000000000))

    # Recording flows into counter arrays
    record_flows(flows, hashes, counter_arrays)
    
    #for array in counter_arrays:
    #    print(array.count(0))
    
    # Estimated size of each flow and calculating error
    flows_estimated_counts, flows_errors =  query_flows(flows, hashes, counter_arrays)

    # Calculating average error
    average_error = 0
    for error in flows_errors:
        average_error += error
    average_error /= len(flows_errors)
    print("Average Error: " + str(average_error))

    # Forming tuple for information output
    flow_information = []
    for index in range(len(flows)):
        flow_information.append((flows_estimated_counts[index], flows[index][0], flows[index][1], flows_errors[index]))
        
    # Sorting by estimated size
    flow_information.sort(reverse = True)

    # Printing 100 largest estimated flows
    for index in range(100):
        print("Flow id: " + str(flow_information[index][1]) + "       Estimated Size: " + str(flow_information[index][0]) + "       Actual Size: " + str(flow_information[index][2]))
# main()


# Inputs: Flows to record, hashes to use for hashing, counter arrays to record in
# Returns: None
# Description: Records a list of flows into a counter array structure. Records to one spot in each counter array
def record_flows(flows, hashes, counter_arrays):
    minus = 0
    plus = 0
    # Recording each flow
    for flow in flows:
        # Creating one int form of flow id to hash
        id_parts = str(flow[0]).split('.')
        flow_id_to_hash = int(id_parts[0] + id_parts[1] + id_parts[2] + id_parts[3])

        # Getting hashed counter locations in each array
        flow_hashed_ids = hash_function(flow_id_to_hash, len(counter_arrays[0]), hashes)

        # Recording in each counter array
        for counter_num in range(len(counter_arrays)):
            # If last bit in hashed key is 1, add the count
            if int(bin(flow_hashed_ids[counter_num])[-1]) == 1:
                plus += 1
                counter_arrays[counter_num][flow_hashed_ids[counter_num]] += int(flow[1])
            # If last bit in hashed key is 0, subtract the count
            else:
                minus += 1
                counter_arrays[counter_num][flow_hashed_ids[counter_num]] -= int(flow[1])

    print(plus)
    print(minus)
# record_flows()


# Inputs: Flows to record, hashes to use for hashing, counter arrays to query
# Returns: Estimated flow sizes, flow count errors
# Description: Query all flows in the counter arrays and calculate error and estimated count
def query_flows(flows, hashes, counter_arrays):
    flows_estimated_counts = []
    flows_errors = []
    
    # Querying each flow
    for flow in flows:

        # Creating one int form of flow id to hash
        id_parts = str(flow[0]).split('.')
        flow_id_to_hash = int(id_parts[0] + id_parts[1] + id_parts[2] + id_parts[3])

        # Getting hashed counter locations in each array
        flow_hashed_ids = hash_function(flow_id_to_hash, len(counter_arrays[0]), hashes)
        
        # Obtaining the count in each counter array
        counts_found = []
        for counter_num in range(len(counter_arrays)):
            if int(bin(flow_hashed_ids[counter_num])[-1]) == 1:
                counts_found.append(counter_arrays[counter_num][flow_hashed_ids[counter_num]])
            else:
                counts_found.append(0-counter_arrays[counter_num][flow_hashed_ids[counter_num]])

        # Sorting the found counts by size
        counts_found.sort()
        #print(counts_found)

        # Estimated count is the median count found
        estimated_count = (counts_found[int(len(counts_found)/2)])
        estimated_error = abs(estimated_count - flow[1])
        #print(flow[1])

        # Recording count and error for this flow
        flows_estimated_counts.append(estimated_count)
        flows_errors.append(estimated_error)
    
    return flows_estimated_counts, flows_errors
# query_flows()


# Inputs: Id of flow to hash, number of counters in the counter array, hashes to use for multi-hashing
# Returns: Index in each counter where flow should be recorded to
# Description: Folding hash function implementation based from https://www.herevego.com/hashing-python/
#   Split number into two (first six digits, and then rest of number)
#       Flow id can be between 4 to 12 digits
#   Add two parts and then do num % num_counter_in_array
def hash_function(flow_id, num_counter_in_array, hashes):
    # Obtaining hash ids
    multi_hashing_flow_ids = []
    for hash in hashes:
        multi_hashing_flow_ids.append(flow_id^hash)
    
    # Obtaining counter positions flow hashes to
    flow_hash_counters = []
    for current_id in multi_hashing_flow_ids:

        # Error if id isn't more than six digits long; correcting here
        if current_id < 1000000:
            current_id += 1000000
        #split_id_sum = int(str(current_id)[:4]) + int(str(current_id)[4:8]) + int(str(current_id)[8:]) # print
        split_id_sum = int(str(current_id)[:6]) + int(str(current_id)[6:])
        flow_hash_counters.append(split_id_sum % num_counter_in_array)

    return flow_hash_counters
# hash_function()


main()