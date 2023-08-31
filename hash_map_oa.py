# Name: Tevin Voong
# OSU Email: voongt@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: 6/9/2023
# Description: Hash Map Implementation - Open Addressing

from a6_include import (DynamicArray, DynamicArrayException, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

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
        Increment from given number to find the closest prime number
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
        Updates key value pairs in the hash map

        param: key and value

        return: None
        """

        hash_value = self._hash_function(key)

        # create loop variable to continue while loop and counter variable for quad probe formula
        loop_variable = 0
        j_counter = 0

        # resizes if table load is less or equal to .5
        if self.table_load() >= .5:
            self.resize_table(self._capacity * 2)

        while loop_variable == 0:
            # quadratic probing formula: (hash function initial index + j^2) + m
            q_probe = (hash_value + (j_counter**2)) % self._capacity

            # sets value if index of the q_probe is None
            if self._buckets[q_probe] is None:
                self._buckets.set_at_index(q_probe, HashEntry(key, value))
                self._size += 1
                return

            # replaces with new value if keys match
            if self._buckets[q_probe].key == key:
                # checks for tombstone
                if self._buckets[q_probe].is_tombstone is True:
                    self._size += 1
                self._buckets.set_at_index(q_probe, HashEntry(key, value))
                return

            # update counter
            j_counter += 1


    def table_load(self) -> float:
        """
        returns the current hash table load factor

        param: None

        return: float indicating table load
        """

        return self.get_size() / self.get_capacity()

    def empty_buckets(self) -> int:
        """
        Method returns number of empty buckets in hash table

        param: None

        return: int of tallied empty buckets
        """

        count = 0

        # loop and tally empty buckets
        for num in range(self._buckets.length()):
            if self._buckets[num] is None:
                count += 1
        return count

    def resize_table(self, new_capacity: int) -> None:
        """
        Changes the capacity of the internal hash table

        param: new capacity

        return: None
        """

        if new_capacity < self.get_size():
            return

        # check if new capacity is a prime number
        if self._is_prime(new_capacity) is False:
            new_capacity = self._next_prime(new_capacity)
            self._capacity = new_capacity
        else:
            self._capacity = new_capacity

        # set size of hash map to 0
        self._size = 0
        # save old bucket and create new empty hash
        old_bucket = self._buckets
        self._buckets = DynamicArray()

        # fill new buckets with None
        for num in range(new_capacity):
            self._buckets.append(None)

        # fill new hash with old hash and account for tombstones
        for num in range(old_bucket.length()):
            values = old_bucket[num]
            if values is not None and values.is_tombstone is False:
                self.put(values.key, values.value)


    def get(self, key: str) -> object:
        """
        Returns value associated with the key

        param: key

        return: value of the key
        """

        hash_value = self._hash_function(key)
        j_counter = 0
        q_probe = (hash_value + (j_counter ** 2)) % self._capacity

        # loops while true
        while self._buckets[q_probe]:
            # quadratic probing formula: (hash function initial index + j^2) + m
            q_probe = (hash_value + (j_counter ** 2)) % self._capacity

            # checks if there is anything at the index provided by the quad probe
            if self._buckets[q_probe] is None:
                return None

            # checks if index is a tombstone
            elif self._buckets[q_probe].is_tombstone is True:
                return None

            # finally checks if the keys are equal then returns value
            elif self._buckets[q_probe].key == key:
                return self._buckets[q_probe].value

            # updates counter for q_probe formula
            j_counter += 1

    def contains_key(self, key: str) -> bool:
        """
        Returns true if key is in the hash and false otherwise

        param: key

        return: bool
        """
        hash_value = self._hash_function(key)
        loop_variable = 0
        j_counter = 0

        # loops continues until a return is encountered
        while loop_variable == 0:
            # quadratic probing formula: (hash function initial index + j^2) + m
            q_probe = (hash_value + (j_counter ** 2)) % self._capacity

            # checks if there is anything at index from quad probe
            if self._buckets[q_probe] is None:
                return False

            # checks if index is a tombstone
            elif self._buckets[q_probe].is_tombstone is True:
                return False

            # finally checks if keys match and returns bool
            elif self._buckets[q_probe].key == key:
                return True

            # updates counter variable for quad probe
            j_counter += 1

    def remove(self, key: str) -> None:
        """
        Removes the given key and its associated value from the hash map

        param: key

        return: None
        """

        hash_value = self._hash_function(key) % self._capacity
        j_counter = 1
        hash_bucket = self._buckets[hash_value]
        while hash_bucket is not None:
            # if bucket matches key and is not a TS, make TS true and decrease size
            if hash_bucket.key == key and hash_bucket.is_tombstone is False:
                hash_bucket.is_tombstone = True
                self._size -= 1
                return
            # implement quad probing in loop if first search did not find the key
            else:
                q_probe = (hash_value + j_counter ** 2) % self._capacity
                j_counter += 1
                hash_bucket = self._buckets[q_probe]

    def clear(self) -> None:
        """
        Clears contents of the hash map

        param: None

        return: None
        """

        # sets buckets to an empty da and appends None to each bucket
        self._buckets = DynamicArray()
        for num in range(self._capacity):
            self._buckets.append(None)
        self._size = 0

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns da with tuples containing key/value pairs

        param: None

        return: da
        """
        arr = DynamicArray()
        # finds buckets that are not empty/not tombstones and appends to the empty da
        for num in range(self._buckets.length()):
            if self._buckets[num] is not None and self._buckets[num].is_tombstone is False:
                arr.append((self._buckets[num].key, self._buckets[num].value))
        return arr

    def __iter__(self):
        """
        Method enables the hash map to iterate across itself

        param: None

        return: None
        """
        self._index = 0

        return self

    def __next__(self):
        """
        Method returns next item in the hash map

        param: None

        return: None
        """

        # try and except method similar to lecture on __next__ method
        try:
            hash_value = self._buckets[self._index]
            # moves to the next item in the hash that isn't None or a TS
            while hash_value is None or hash_value.is_tombstone is True:
                self._index = self._index + 1
                hash_value = self._buckets[self._index]
        except DynamicArrayException:
            raise StopIteration

        self._index = self._index + 1
        return hash_value

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

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(25, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        if m.table_load() > 0.5:
            print(f"Check that the load factor is acceptable after the call to resize_table().\n"
                  f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")

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
    m = HashMap(11, hash_function_1)
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

    print("\nPDF - remove example 2")
    print("----------------------")
    m = HashMap(223, hash_function_1)
    print(m.get('key265'))
    m.put('key1', 779)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))

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

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.resize_table(2)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(12)
    print(m.get_keys_and_values())

    print("\nPDF - __iter__(), __next__() example 1")
    print("---------------------")
    m = HashMap(10, hash_function_1)
    for i in range(5):
        m.put(str(i), str(i * 10))
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)

    print("\nPDF - __iter__(), __next__() example 2")
    print("---------------------")
    m = HashMap(10, hash_function_2)
    for i in range(5):
        m.put(str(i), str(i * 24))
    m.remove('0')
    m.remove('4')
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)
