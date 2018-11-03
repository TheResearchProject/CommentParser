import unittest

class ComparisonSyntaxException(Exception):
    pass
    
class InvalidValueFormatException(Exception):
    pass    
    
class InvalidComparisonException(Exception):
    pass    

class InvalidRangeException(Exception):
    pass        
    
def comparator(comparison, value):
    """
    This function will receive input in the following formats:
    - '="a_string"': will compare value with the string between quotes,
                     and return True if they are equal, False otherwise
    - '=number', '!=number', '>number', '<number', '>=number', '<=number':
                     will compare the value with the number that 
                     exists after the comparison operator. Will return True
                     if the comparison is succesful, False otherwise
    - 'number1<X<number2', 'number1<=X<number2', 'number1<=X<=number2':
                     will check if value (represented in the comparison variable
                     as 'X') is within the range specified. Returns True if 
                     value in inside the range, False otherwise.
    - If comparison is not a valid format, should raise a ComparisonSyntaxException.
    - If value is not a number or not a string, should raise a InvalidValueFormatException.
    - If comparison is expecting a string and value is a number, or vice-versa, should
      raise a InvalidComparisonException.
    - If in a range comparison, number2 is smaller than number1, raise InvalidRangeException.
    """
    if comparison[0:2] == '="':
        if comparison[2:-1] == value:
            return True
        else:
            return False
    elif comparison[0:1] == '=':
        if int(comparison[1:]) == value:
            return True
        else:
            return False
    elif comparison[0:2] == '!=':
        if int(comparison[2:]) != value:
            return True
        else:
            return False
    elif comparison[0:2] == '>=':
        if int(comparison[2:]) <= value:
            return True
        else:
            return False 
    elif comparison[0:2] == '<=':
        if int(comparison[2:]) >= value:
            return True
        else:
            return False 
    elif comparison[0:1] == '>':
        if int(comparison[1:]) < value:
            return True
        else:
            return False
    elif comparison[0:1] == '<':
        if int(comparison[1:]) > value:
            return True
        else:
            return False        
    elif comparison.find('<=X<=') > -1:
        (a, b) = comparison.split('<=X<=')
        if int(a) <= value <= int(b):
            return True
        else:
            return False       
    elif comparison.find('<=X<') > -1:
        (a, b) = comparison.split('<=X<')
        if int(a) <= value < int(b):
            return True
        else:
            return False 
    elif comparison.find('<X<=') > -1:
        (a, b) = comparison.split('<X<=')
        if int(a) < value <= int(b):
            return True
        else:
            return False
    elif comparison.find('<X<') > -1:
        (a, b) = comparison.split('<X<')
        if int(a) < value < int(b):
            return True
        else:
            return False
    else:
        raise ComparisonSyntaxException()

               
class TestComparator(unittest.TestCase):
  

    def test_equal_string(self):
        self.assertTrue(comparator('="Spam"', 'Spam'))
        self.assertFalse(comparator('="Spam"', 'Eggs'))
        self.assertTrue(comparator('="Spam and eggs"', 'Spam and eggs'))
        self.assertFalse(comparator('="Spam and eggs"', 'Eggs and spam'))
    
    
    def test_number_comparison(self):
        self.assertTrue(comparator('=2', 2))
        self.assertTrue(comparator('=-3', -3))
        self.assertTrue(comparator('!=5', 11))
        self.assertTrue(comparator('!=-14', -19))
        self.assertTrue(comparator('>200', 402))
        self.assertTrue(comparator('>-300', 605))
        self.assertTrue(comparator('<123', -22))
        self.assertTrue(comparator('<-2376', -7777))
        self.assertTrue(comparator('>=302', 1024))
        self.assertTrue(comparator('>=-2310', -715))
        self.assertTrue(comparator('<=432', 103))
        self.assertTrue(comparator('<=-674', -7940))
        
        self.assertFalse(comparator('=4', 3))
        self.assertFalse(comparator('=-8', -5))
        self.assertFalse(comparator('!=13', 13))
        self.assertFalse(comparator('!=-16', -16))
        self.assertFalse(comparator('>500', 233))
        self.assertFalse(comparator('>-92', -522))
        self.assertFalse(comparator('<546', 7765))
        self.assertFalse(comparator('<-2376', -2375))
        self.assertFalse(comparator('>=211', 103))
        self.assertFalse(comparator('>=-463', -495))
        self.assertFalse(comparator('<=432', 2103))
        self.assertFalse(comparator('<=-674', -40))      
        
    
    def test_range(self):
        #Positive Tests
        self.assertTrue(comparator('1<X<10', 9))
        self.assertTrue(comparator('-3<X<200', 66))
        self.assertTrue(comparator('-800<X<-600', -650))
        
        self.assertTrue(comparator('15<=X<20', 15))
        self.assertTrue(comparator('-96<=X<424', -23))
        self.assertTrue(comparator('-24<=X<-8', -20))
        self.assertTrue(comparator('-24<=X<-8', -24))
        
        self.assertTrue(comparator('35<X<=40', 37))
        self.assertTrue(comparator('-6<X<=4', 0))
        self.assertTrue(comparator('-6<X<=4', -5))
        self.assertTrue(comparator('-92<X<=-48', -63))
        self.assertTrue(comparator('-92<X<=-48', -48))
        
        self.assertTrue(comparator('35<=X<=40', 35))
        self.assertTrue(comparator('-6<=X<=4', 4))
        self.assertTrue(comparator('-6<=X<=4', -2))
        self.assertTrue(comparator('-6<=X<=4', -6))
        self.assertTrue(comparator('-92<=X<=-48', -84))
        self.assertTrue(comparator('-92<=X<=-48', -48))      
      
        #Negative Tests
        self.assertFalse(comparator('1<X<10', 0))
        self.assertFalse(comparator('1<X<10', 10))
        self.assertFalse(comparator('-3<X<200', 600))
        self.assertFalse(comparator('-800<X<-600', -6650))
        
        self.assertFalse(comparator('15<=X<20', 20))
        self.assertFalse(comparator('15<=X<20', 14))
        self.assertFalse(comparator('-96<=X<424', -567))
        self.assertFalse(comparator('-24<=X<-8', -8))
        self.assertFalse(comparator('-24<=X<-8', 240))
        
        self.assertFalse(comparator('35<X<=40', 35))
        self.assertFalse(comparator('35<X<=40', 41))
        self.assertFalse(comparator('-6<X<=4', -6))
        self.assertFalse(comparator('-6<X<=4', 5))
        self.assertFalse(comparator('-92<X<=-48', -92))
        self.assertFalse(comparator('-92<X<=-48', -47))
        
        self.assertFalse(comparator('35<=X<=40', 34))
        self.assertFalse(comparator('35<=X<=40', 41))
        self.assertFalse(comparator('-6<=X<=4', -7))
        self.assertFalse(comparator('-6<=X<=4', 5))
        self.assertFalse(comparator('-92<=X<=-48', -93))
        self.assertFalse(comparator('-92<=X<=-48', -47))   

if __name__ == '__main__':
    unittest.main()
    