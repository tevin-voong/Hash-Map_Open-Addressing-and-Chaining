# Name: Tevin Voong
# OSU Email: voongt@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: 6/9/2023
# Description: Hash Map Implementation - Chaining


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number and the find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Updates key/value pair in the hash map

        param: key and value

        return: None
        """

        # resizes if table load is less or equal to 1
        if self.table_load() >= 1:
            self.resize_table(self._capacity * 2)

        h_value = self._hash_function(key)
        h_index = h_value % self.get_capacity()
        hash_linked_list = self._buckets[h_index]

        # if the linked list at the index of the hash map contains the key, remove the key
        if hash_linked_list.contains(key):
            hash_linked_list.remove(key)
            self._size -= 1

        hash_linked_list.insert(key, value)
        self._size += 1

    def empty_buckets(self) -> int:
        """
        Method returns the number of empty buckets

        param: none

        return: int representing number of empty buckets
        """

        empty_buckets = 0

        # loops through and tallies buckets that have length of 0
        for num in range(self.get_capacity()):
            if self._buckets[num].length() == 0:
                empty_buckets += 1

        return empty_buckets

    def table_load(self) -> float:
        """
        Returns current load factor of hash table

        param: None

        return: float indicating load factor
        """
        return self._size / self._capacity

    def clear(self) -> None:
        """
        Clear hash map contents

        param: None

        return: None
        """

        self._buckets = DynamicArray()
        # appends an empty linked list to each index to clear hash map
        for num in range(self._capacity):
            self._buckets.append(LinkedList())
        self._size = 0

    def resize_table(self, new_capacity: int) -> None:
        """
        Changes capacity of the internal hash table

        param: new capacity

        return: None
        """

        hash_map = self._buckets

        # if new capacity is less than zero, do nothing
        if new_capacity < 1:
            return

        # if new capacity is not prime, make it the next prime
        if self._is_prime(new_capacity) is False:
            self._capacity = self._next_prime(new_capacity)

        else:
            self._capacity = new_capacity

        self._buckets = DynamicArray()
        # appends an empty linked list to each index to clear hash map
        for num in range(self._capacity):
            self._buckets.append(LinkedList())
        self._size = 0

        for indices in range(hash_map.length()):
            hash_linked_list = hash_map[indices]
            # adds in the ll if there is one at the index
            if hash_linked_list.length() is not None:
                for add_node in hash_linked_list:
                    self.put(add_node.key, add_node.value)

    def get(self, key: str):
        """
        Method returns value associated with key

        param: key

        return: str value
        """

        h_value = self._hash_function(key)
        h_index = h_value % self.get_capacity()

        # returns value if the keys match at the hash index
        if self._buckets[h_index].contains(key) is not None:
            return self._buckets[h_index].contains(key).value

        else:
            return None

    def contains_key(self, key: str) -> bool:
        """
        Returns true if key is in the hash map, false otherwise

        param: key

        return: bool
        """

        h_value = self._hash_function(key)
        h_index = h_value % self.get_capacity()

        # return true if the hash index contains the right key
        if self._buckets[h_index].contains(key) is not None:
            return True
        else:
            return False

    def remove(self, key: str) -> None:
        """
        Removes key from the hash map

        param: key

        return: None
        """

        h_value = self._hash_function(key)
        h_index = h_value % self.get_capacity()

        # removes key if true
        if self._buckets[h_index].remove(key):
            self._size -= 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns an arr containing tuples of the key/value pairs in the hash map

        param: None

        return: arr
        """
        arr = DynamicArray()

        # loops through buckets and lls in buckets to append key/value pairs
        for indices in range(self._buckets.length()):
            for ll in self._buckets[indices]:
                arr.append((ll.key, ll.value))

        return arr


def find_mode(da: DynamicArray) -> (DynamicArray, int):
    """
    Method finds the mode and frequency

    param: da

    return: da of the mode(s) and the frequency
    """
    # if you'd like to use a hash map,
    # use this instance of your Separate Chaining HashMap
    map = HashMap(da.length())
    key_frequency = 0
    arr = DynamicArray()

    # loop through arr and create a hash map with keys as an item and values as frequency of item
    for indicies in range(da.length()):
        hash_key = da[indicies]
        hash_value = map.get(hash_key)

        if hash_value is None:
            hash_value = 1
            map.put(hash_key, hash_value)

        # if there is a value, add to hash map and keep track of how many
        elif hash_value is not None:
            hash_value += 1
            map.put(hash_key, hash_value)

        # if value is equal to frequency, append to arr and frequency stays the same
        if hash_value == key_frequency:
            arr.append(hash_key)

        # if value is greater than frequency, append to a new arr and set new frequency
        elif hash_value > key_frequency:
            arr = DynamicArray()
            key_frequency = hash_value
            arr.append(hash_key)

    return arr, key_frequency


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(23, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(53, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
    print(m.get_keys_and_values())

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")
