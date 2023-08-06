class SeaSor:

    '''
        Parent class for several
        searching & sorting
        algorithms;
        parameter are optional;
    '''    

    def __init__(self, array=None, target=None):

        self.array = array
        self.target = target

    def get_int_array(self, length=10, maxnum=10):

        import random

        ''' Creates arrays with
            optional length and 
            random numbers;
            returns also a random
            choice of the created
            list to test previous
            methods;
        '''
        rand_array = []

        for i in range(length):
            n = random.randrange(maxnum)
            rand_array.append(n)

        include_num = random.choice(rand_array)

        return rand_array, include_num

    def get_ascii_array(self, length=10, charset='a'):

        ''' Method to create 
            random ascii array;
            Optional parameters,
             second is for defining
             kind of charset;
            return list and 
             chosen element;
        '''

        import random
        import string

        rand_array = []

        if charset == 'll':        # 'll' for low letters
            chars = string.ascii_lowercase

        elif charset == 'ul':      # 'ul' for upper letters
            chars = string.ascii_uppercase

        elif charset == 'pt':      # 'pt' for punctuation
            chars = string.punctuation

        elif charset == 'pb':      # 'pb' for printable
            chars = string.printable


        for _ in range(length):
            char = random.choice(chars)
            rand_array.append(char)

        include_elem = random.choice(rand_array)

        return rand_array, include_elem

    def rm_dupls(self, array=None):

        ''' This method removes
            duplicates from list;
            returns a list without
            duplicates;
        '''

        if array == None:
            array = self.array

        unique = []            # new list without dupl
        for item in array:
            if item not in unique:
                unique.append(item)

        return unique

# maybe solivng this mess with @classmethod ?!
class WriteRead(SeaSor):

    ''' Writing and reading
        lists and results to
        a file;
        Random lists are
        dumped to json;
    '''

    def __init__(self, array=None, target=None, sor_array=None, index=None):

        super().__init__(array, target)
        self._sor_array = sor_array
        self._index = index

    @property
    def sor_array(self):
        return self._sor_array

    @sor_array.setter
    def sor_array(self, sor_array):
        self._sor_array = sor_array

    @property
    def index(self):
        return self._index

    @index.setter
    def index(self, index):
        self._index = index

    def write_seasor(self):

        ''' Writing results
            to a txt file;
        '''
        with open('SearchSort.txt', 'a') as seso:
            seso.write(f'''\n
Array:          {self.array}
Target:         {self.target}
Index:          {self._index}
Sorted Array:   {self._sor_array}
        \n\n''')

    def write_arr(self):

        ''' This method appends
            test arrays to
            json stream;
        '''
        import json

        with open('myLists.json', 'a') as ml:
            json.dump(self.array[0], ml)
            ml.write('\n')

    def write_test(self):

        ''' Appends list containing
            random lists + randomly
            chosen target to
            myTests.json;
        '''
        import json

        with open('myTests.json', 'a')as mt:
            json.dump(self.array, ml)
            ml.write('\n')

    def read_seasor(self):
        pass


class Sort(SeaSor):

    '''
        Subclass of SearchSort;
    '''

    def __init__(self, array=None, target=None):
        super().__init__(array, target)

    def bubble(self, array=None):
        ''' Uses bubble sort algorithm,
            not recommended, as the runtime
            is not good;
        '''
        if array == None:
            array = self.array

        for i in range(len(array)):
            for j in range(len(array)-i-1):
                # if index j bigger than j+1 -> exchange
                if array[j] > array[j+1]:
                    array[j], array[j+1] = array[j+1], array[j]
        return array

    def quick(self, array=None):
        ''' Private class method;
            sorts an array;
            can take the self or 
            an optional parameter;
        '''
        # if no func parameter, take self.*
        if array == None:
            array = self.array

        #recursive method
        def sort_my_array(array):
            '''
                Nested func so we do
                not have to care about
                self or optional parameter;
            '''
            if len(array) <= 1:
                return array
            else:
                pivot = array.pop()

                smaller = []    # smaller than pivot
                bigger = []     # bigger than pivot

            for i in array:
                if i < pivot:
                    smaller.append(i)
                else:
                    bigger.append(i)
            return sort_my_array(smaller) + [pivot] + sort_my_array(bigger)

        return sort_my_array(array)

    
class Search(Sort):

    '''
        Subclass of Sort;
        inherits from
        class Sort (so also
        from class SearchSort);
    '''

    def __init__self(array=None, target=None):
        super().__init__(array, target)

    def bin_index(self, array=None, target=None):
        ''' Binary search method;
            recursively;
            needs sorted list;
            returns falls if item not in list;
        '''
        if array == None:
            array = self.array
            target = self.target

        start, end = 0,  (len(array)-1)
        found = False
        while start <= end and not found:
            mid = ((start + end) // 2)
            if array[mid] == target:
                found = True
                return mid
            elif target < array[mid]:
                end = mid - 1
            elif target > array[mid]:
                start = mid + 1
        return False

    def hash_index(self, array = None, target = None):    
        ''' Search in hashmap;
            checks value for value;
            returns false if item not in list;
        '''
        if array == None:
            array = self.array
            target = self.target

        for _ in range(len(array)):
            for p, n in enumerate(array):
                if n == target:
                    return p
        return False

    def lin_index(self, array=None, target=None):
        '''
            Iterates over positions
            one by one and returns postion
            if found, otherwise false;
        '''
        if array == None:
            array = self.array
            target = self.target

        for pos in range(len(array)):
            if array[pos] == target:
                return pos
        return False
