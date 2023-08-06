import random

class SearchSort:

    '''
        Parent class for several
        searching & sorting
        algorithms;
        parameter are optional;
    '''    

    def __init__(self, array=None, target=None):

        self.array = array
        self.target = target


    def get_int_array(self, length=100, maxnum=10):
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


class Sort(SearchSort):

    '''
        Subclass of SearchSort;
    '''

    def __init(self, array=None, target=None):
        super().__init__(array, target)


    def bubble_sort_array(self, array=None):
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

    def quick_sort_array(self, array=None):
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

    def binary_search_indexarray(self, array=None, target=None):
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

    def hash_search_indexarray(self, array = None, target = None):    
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

    def linear_search_indexarray(self, array=None, target=None):
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