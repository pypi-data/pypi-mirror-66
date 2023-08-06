#!/usr/bin/python

import re
from sys import argv

def clean_param_value(param_value):
    if param_value.isdigit(): return int(param_value)
    elif param_value.isdecimal(): return float(param_value)
    return param_value

def get_declaration(variable_name, variable_value):
    if (isinstance(variable_value, str)):
        return variable_name + " = '" + variable_value + "'"
    elif(isinstance(variable_value, int) or isinstance(variable_value, float)):
        return variable_name + " = " + str(variable_value)

def find_class_declarations(source_code, class_name):
    pattern = '(?P<indent>[ \t]*)(class ' + class_name + '(.|\n){10,}?)(?<! )(?:\n)(?P=indent)?(?! )'
    regex = re.compile(pattern, re.MULTILINE)
    return re.finditer(regex, source_code)

def find_class_instantiations(source_code, variable_name):
    regex = re.compile(variable_name + "\([^\)]*\)", re.MULTILINE)
    return re.finditer(regex, source_code)

def find_parameter(source_code, parameter_name):
    param_regex = re.compile("(, ?)?" + parameter_name + " ?= ?[^,)]*")
    return re.search(param_regex, source_code)

def find_all_named_parameters(source_code):
    param_regex = re.compile("(, ?)?[A-Za-z_]+ ?= ?[^,)]*")
    return re.finditer(param_regex, source_code)

def declare_variable(source_code, variable_name, variable_value):
    lines = source_code.split("\n")
    lines.append(get_declaration(variable_name, variable_value))
    return "\n".join(lines)

def add_param_to_class_instantiation(source_code, class_name, new_parameter_name, new_parameter_value):
    original = source_code
    offset = 0
    for old_instantiation in find_class_instantiations(source_code, class_name):
        old_instantiation_text = old_instantiation.group()

        # get text for line
        old_start, old_end = old_instantiation.span()
        start = old_start + offset
        end = old_end + offset
        before = source_code[:start]
        after = source_code[end:]

        #line = original[before.rindex("\n") if "\n" in before else 0: len(before) + len(old_instantiation_text) + (after.index("\n") if "\n" in after else len(after) - 1)].strip()
        line = before[before.rindex("\n") + 1 if "\n" in before else 0:] + old_instantiation_text + after[:after.index("\n") if "\n" in after else len(after) - 1].strip("\n")

        params = {}
        for match in find_all_named_parameters(old_instantiation_text):
            param_name, param_value = match.group().replace(",", "").strip().split("=")
            param_value = clean_param_value(param_value)
            params[param_name] = param_value

        if str(type(new_parameter_value)) in ["<type 'function'>", "<class 'function'>"]:
            new_parameter_value_for_instantiation = new_parameter_value({ "params": params, "line": line, "text": old_instantiation_text, "start": old_start, "end": old_end, "source_code": original })
        else:
            new_parameter_value_for_instantiation = new_parameter_value

        if isinstance(new_parameter_value_for_instantiation, int) or isinstance(new_parameter_value_for_instantiation, float):
            insertion = new_parameter_name + "=" + str(new_parameter_value_for_instantiation)
        elif isinstance(new_parameter_value_for_instantiation, str):
            insertion = new_parameter_name + "=" + '"' + new_parameter_value_for_instantiation + '"'

        if old_instantiation_text.count(",") > 0:
            insertion = ", " + insertion

        # find end of class instantiation parentheses
        insert_here = old_instantiation_text.rindex(')')
        new_instantiation_text = old_instantiation_text[:insert_here] + insertion + old_instantiation_text[insert_here:]
        source_code = before + new_instantiation_text + after
        offset += len(new_instantiation_text) - len(old_instantiation_text)
    return source_code

def remove_class_instantiation_parameter(source_code, class_name, parameter_name, condition=None):
    offset = 0
    for class_instantiation in find_class_instantiations(source_code, class_name):
        old_instantiation = class_instantiation.group()
        match = find_parameter(old_instantiation, parameter_name)
        params_padded = class_name + "( " in old_instantiation

        if match:
            # get paramter value
            param_value = match.group().split("=")[1].strip()
            param_value = clean_param_value(param_value)

            if condition is None or condition(param_value):
                match_start, match_end = match.span()
                new_instantiation = old_instantiation[:match_start] + old_instantiation[match_end:]
                # remove comma from second param if replaced first param
                if class_name + "(, " in new_instantiation:
                    if params_padded:
                        new_instantiation = new_instantiation.replace(class_name + "(,", class_name + "(")
                    else:
                        new_instantiation = new_instantiation.replace(class_name + "(, ", class_name + "(")
                elif class_name + "(," in new_instantiation:
                    new_instantiation = new_instantiation.replace(class_name + "(,", class_name + "(")
                start_removal = class_instantiation.span()[0] - offset
                end_removal = class_instantiation.span()[1] - offset
                source_code = source_code[:start_removal] + new_instantiation + source_code[end_removal:]
                offset += (len(old_instantiation) - len(new_instantiation))

    return source_code
        

def remove_comments(source_code):
    lines = source_code.split("\n")
    lines = [line for line in lines if not line.startswith("#")]
    return "\n".join(lines)

def remove_imports(source_code):
    lines = source_code.split("\n")
    lines = [line for line in lines if not line.startswith("from ")]
    return "\n".join(lines)

def replace_class(source_code, old_class_name, new_class_name, condition=None):
    if condition:
        original = source_code
        offset = 0
        for old_instantiation in find_class_instantiations(source_code, old_class_name):
            old_instantiation_text = old_instantiation.group()
            start = old_instantiation.span()[0] + offset
            end = old_instantiation.span()[1] + offset
            before = source_code[:start]
            after = source_code[end:]
            line = original[before.rindex("\n") if "\n" in before else 0: len(before) + len(old_instantiation_text) + (after.index("\n") if "\n" in after else len(after) - 1)]
            if condition({ "text": old_instantiation_text, "line": line }):
                new_instantiation = old_instantiation_text.replace(old_class_name, new_class_name)
                source_code = before + new_instantiation + after
                offset += len(new_instantiation) - len(old_instantiation_text)
        return source_code
    else:
        return source_code.replace(old_class_name + "(", new_class_name + "(")

def replace_variable_declaration(source_code, variable_name, new_variable_value):
    old_lines = source_code.split("\n")
    new_lines = []
    for line in old_lines:
        if (line.startswith(variable_name + ' =') or line.startswith(variable_name + '=')) :
            new_lines.append(get_declaration(variable_name, new_variable_value))
        else:
            new_lines.append(line)
    return "\n".join(new_lines)

def remove_class_declaration(source_code, class_name):
    offset = 0
    for class_declaration in find_class_declarations(source_code, class_name):
        declaration_text = class_declaration.group()

        # get text for line
        old_start, old_end = class_declaration.span()
        start = old_start + offset
        end = old_end + offset
        before = source_code[:start]
        after = source_code[end:]

        source_code = before + after
        offset -= len(declaration_text)
    return source_code

if __name__ == '__main__':
    cmd, fp, subcommand, param1, param2 = argv
    with open(fp) as f:
        source_code = f.read().decode()
    if (subcommand == "remove-comments"):
        source_code = remove_comments(source_code)
        with open(fp, "w") as f:
            f.write(source_code)
    elif (subcommand == "remove-imports"):
        source_code = remove_imports(source_code)
        with open(fp, "w") as f:
            f.write(source_code)
    elif (subcommand == "declare-variable"):
        source_code = declare_variable(source_code, param1, param2)
        with open(fp, "w") as f:
            f.write(source_code)
    elif (subcommand == "remove-class-declaration"):
        source_code = remove_class_declaration(source_code, param1)
        with open(fp, "w") as f:
            f.write(source_code)
