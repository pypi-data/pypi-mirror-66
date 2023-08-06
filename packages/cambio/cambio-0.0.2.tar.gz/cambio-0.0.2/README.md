# cambio
Change Python Source Code Files

# usage
## Remove Comments
```python
from cambio import remove_comments

with open("example.py") as f:
    text = f.read()

text = remove_comments(text)

with open("example_without_comments.py", "w") as f:
    f.write(text)
```

```bash
cambio example.py remove-comments
```

## Remove Imports
```python
from cambio import remove_imports

with open("example.py") as f:
    text = f.read()

text = remove_imports(text)

with open("example_without_imports.py", "w") as f:
    f.write(text)
```

```bash
cambio example.py remove-imports
```

## Declare Variable
```python
from cambio import declare_variable
from django.utils.crypt import get_random_string 

with open("settings.py") as f:
    text = f.read()

text = declare_variable(text, "SECRET_KEY", get_random_string())

with open("settings.py", "w") as f:
    f.write(text)
```

```bash
cambio settings.py declare-variable "SECRET_KEY" "$(uuidgen)"
```

## Replace Class
```python
from cambio import replace_class

code = "my_fruit = Apple()"

new_code = replace_class(code, "Apple", "Orange")
print(new_code)
# my_smoothie = Orange()
```

```bash
cambio juicer.py replace-class "Apple" "Orange"
```

## Replace Variable Declaration
```python
from cambio import replace_variable_declaration

code = "HTTP_ORIGIN = 'http://localhost:8000'"
new_code = replace_variable_declaration('HTTP_ORIGIN', 'http://localhost:4200')
print(new_code)
# HTTP_ORIGIN = 'http://localhost:4200'
```
```bash
cambio settings.py replace-declaration 'HTTP_ORIGIN' 'http://localhost:4200'
```

## Remove Class Instantiation Parameter
```python
from cambio import remove_class_instantiation_parameter

old_code = "my_drink = Wine(age=100)"
new_code = remove_class_instantiation_parameter(old_code, 'Wine', 'age')
print(new_code)
# my_drink = Wine()
```
```bash
cambio settings.py
```

## Conditionally Remove Class Instantiation Parameter
```python
from cambio import remove_class_instantiation_parameter

old_code = "bottle_1 = Wine(age=100)\nbottle_2 = Wine(age=1)"
# removes all bottles under 10 years of age
new_code = remove_class_instantiation_parameter(old_code, 'Wine', 'age', lambda age: age < 10)
print(new_code)
# bottle_1 = Wine(age=100)\n
```
```bash
cambio settings.py
```

## Add Parameter to Class Instantiation
```python
from cambio import add_param_to_class_instantiation

old_code = "[Food(type='Cereal')\n, Fruit(type='Cheese')]"

def get_expiration(instantiation):
    text = instantiation['text']
    if 'Cereal' in text:
        return 10
    elif 'Cheese' in text:
        return 1

# age cars by one year
add_param_to_class_instantiation(old_code, "Fruit", "expiration", get_expiration)
```

## Remove Class Declaration
```python
from cambio import remove_class_declaration

old_code = '''
class OldCar():
    a = 1
    b = 2

class NewCar():
    a = 1
    b = 2
'''

new_code = remove_class_declaration(old_code, "OldCar")
```

```bash
cambio example.py remove-class-declaration 'OldCar'
```

# Testing
To test the package run
```
python3 -m unittest cambio.tests.test
```

## Support
Contact the Library Author, Daniel J. Dufour, or post an issue at https://github.com/danieljdufour/cambio/issues

