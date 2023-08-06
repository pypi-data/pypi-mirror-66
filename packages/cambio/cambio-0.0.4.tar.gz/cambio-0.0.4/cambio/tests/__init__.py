#-*- coding: utf-8 -*-
from unittest import main, TestCase
from cambio import add_param_to_class_instantiation
from cambio import find_all_named_parameters
from cambio import remove_class_definition
from cambio import remove_class_instantiation_parameter
from cambio import remove_comments
from cambio import remove_imports
from cambio import declare_variable
from cambio import replace_class
from cambio import replace_variable_declaration

class TestRemovingClassDeclaration(TestCase):
    def test_removing_multi_line_class_declaration(self):
        old_code = '''
        class A():
            prop1 = 1
            prop2 = 2
            prop3 = 3

        class B():
            prop1 = 1
            prop2 = 2
            prop3 = 3

        class C():
            prop1 = 1
            prop2 = 2
            prop3 = 3

        '''
        new_code = remove_class_definition(old_code, "B")
        expected_code = '''
        class A():
            prop1 = 1
            prop2 = 2
            prop3 = 3


        class C():
            prop1 = 1
            prop2 = 2
            prop3 = 3

        '''
        self.assertEqual(new_code, expected_code)

class TestRemovingComments(TestCase):
    def test_removing_comments(self):
        old_code = "# here's a comment\n\nprint('hello')"
        new_code = remove_comments(old_code)
        self.assertEqual(new_code.strip(), "print('hello')")

class TestRemovingImports(TestCase):
    def test_removing_imports(self):
        old_code = "from non_existent_package import non_existent_module\n\nfruit='apple'"
        code_without_imports = remove_imports(old_code)
        exec(code_without_imports.strip())

class TestDeclaringVariable(TestCase):
    def test_declaring_string(self):
        old_settings = "from sys import version_info\npython_version = version_info.major"
        new_settings = declare_variable(old_settings, "SECRET_KEY", '123456789')
        self.assertTrue(new_settings, "from sys import version_info\nSECRET_KEY = '12345678'\npython_version = version_info.major")

    def test_declaring_float(self):
        old_settings = "from sys import version_info\npython_version = version_info.major"
        new_settings = declare_variable(old_settings, "SECRET_NUMBER", 123456789)
        self.assertTrue(new_settings, "from sys import version_info\nSECRET_NUMBER = 12345678\npython_version = version_info.major")

class TestReplacingClass(TestCase):
    def test_replacing_class(self):
        old_code = "my_fruit = Apple(age=1)"
        new_code = replace_class(old_code, "Apple", "Orange")
        self.assertEqual(new_code, "my_fruit = Orange(age=1)")

    def test_conditionally_replacing_class(self):
        old_code = "fruits = [new Apple(old=False), new Apple(old=True)]"
        new_code = replace_class(old_code, "Apple", "Orange", lambda data : 'old=True' in data['text'])
        self.assertEqual(new_code, "fruits = [new Apple(old=False), new Orange(old=True)]")

class TestReplacingVariableDeclaration(TestCase):
    def test_replacing_variable_declaration(self):
        old_code = "HTTP_ORIGIN = 'http://localhost:8000'"
        new_code = replace_variable_declaration(old_code, 'HTTP_ORIGIN', 'http://localhost:4200')
        self.assertEqual(new_code, "HTTP_ORIGIN = 'http://localhost:4200'")

class TestFindingsClassInstantiationParameters(TestCase):
    def test_finding_class_instantiation_parameters(self):
        old_code = 'new Fruit(age_in_days=5, type="Apple", country="USA")'
        params = [match.group() for match in find_all_named_parameters(old_code)]
        self.assertEqual(str(params), str(['age_in_days=5', ', type="Apple"', ', country="USA"']))

class TestAddingParamToClassInstantiation(TestCase):
    def test_adding_param_to_class_instantiation_with_one_param(self):
        old_code = 'new Fruit(country_code="USA")'
        new_code = add_param_to_class_instantiation(old_code, 'Fruit', 'type', 'Apple')
        self.assertEqual(new_code, 'new Fruit(country_code="USA", type="Apple")')

    def test_adding_param_to_class_instantiation(self):
        old_code = 'new Fruit(age_in_days=5, type="Apple", country="USA")'
        new_code = add_param_to_class_instantiation(old_code, 'Fruit', 'quality', '100')
        self.assertEqual(new_code, 'new Fruit(age_in_days=5, type="Apple", country="USA", quality="100")')

    def test_adding_calculated_param_to_class_instantiation(self):
        old_code = 'new Fruit(age_in_days=5, type="Apple", country="USA")'
        new_code = add_param_to_class_instantiation(old_code, 'Fruit', 'expiration', lambda data: 10 if 'Apple' in data['line'] else 1)
        self.assertEqual(new_code, 'new Fruit(age_in_days=5, type="Apple", country="USA", expiration=10)')

    def test_conditionally_adding_param_to_class_instantiation(self):
        old_code ='''
        class Breakfast:
            origin = new Egg()
        
        class Lunch:
            origin = new Egg()
        '''
        new_code = add_param_to_class_instantiation(old_code, 'Egg', 'scrambled', True, lambda data : data['before'].rindex(' Breakfast') > data['before'].rindex('class'))
        self.assertEqual(new_code, '''
        class Breakfast:
            origin = new Egg(scrambled=True)
        
        class Lunch:
            origin = new Egg()
        ''')



class TestRemovingClassInstantiationParameter(TestCase):
    def test_removing_when_only_one_parameter(self):
        old_code = "my_car = Car(age=10)\nyour_car = Car(age=2)"
        new_code = remove_class_instantiation_parameter(old_code, 'Car', 'age')
        self.assertEqual(new_code, 'my_car = Car()\nyour_car = Car()')

    def test_removing_when_multiple_parameter(self):
        old_code = "my_car = Car(age=10, make='Ford')\nyour_car = Car(year=2020, age=2)"
        new_code = remove_class_instantiation_parameter(old_code, 'Car', 'age')
        self.assertEqual(new_code, "my_car = Car(make='Ford')\nyour_car = Car(year=2020)")

    def test_removing_when_multiple_parameter(self):
        old_code = "my_car = Car(age=10, make='Ford')\nyour_car = Car(year=2020, age=2)"
        new_code = remove_class_instantiation_parameter(old_code, 'Car', 'age')
        self.assertEqual(new_code, "my_car = Car(make='Ford')\nyour_car = Car(year=2020)")

    def test_conditionally_removing_parameter(self):
        old_code = "bottle_1 = Wine(age=100)\nbottle_2 = Wine(age=1)"
        # removes all bottles under 10 years of age
        new_code = remove_class_instantiation_parameter(old_code, 'Wine', 'age', lambda age: age < 10)
        self.assertEqual(new_code, "bottle_1 = Wine(age=100)\nbottle_2 = Wine()")

if __name__ == '__main__':
    main()