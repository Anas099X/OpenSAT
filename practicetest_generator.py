import json
import random
import requests

# Function to collect questions from the external API
def question_collecter(section, domain, num):
    """
    Collects 'num' random questions from the specified 'section' and 'domain'.
    """
    question_objects = requests.get(
        'https://api.jsonsilo.com/public/942c3c3b-3a0c-4be3-81c2-12029def19f5'
    ).json()

    collected_nums = [index for index, question in enumerate(question_objects[section], start=1)
                      if question.get('domain') == domain]

    return (random.sample(collected_nums, num) if len(collected_nums) >= num
            else collected_nums)

# Function to open and modify JSON data
def open_and_modify(file_path, path, new_value, append=False, create_if_missing=False):
    with open(file_path, 'r') as file:
        data = json.load(file)

    # Navigate through the nested structure using the path
    current = data
    for i, key in enumerate(path[:-1]):
        if isinstance(current, dict):
            if key not in current:
                if create_if_missing:
                    current[key] = {} if isinstance(path[i + 1], str) else []
                else:
                    raise KeyError(f"Key '{key}' not found in the dictionary.")
            current = current[key]
        elif isinstance(current, list):
            if isinstance(key, int) and 0 <= key < len(current):
                current = current[key]
            else:
                raise IndexError(f"Index '{key}' out of range.")
        else:
            raise TypeError("Intermediate elements must be dicts or lists.")

    # Modify the final element in the path
    last_key = path[-1]
    if isinstance(current, dict):
        if last_key in current:
            if isinstance(current[last_key], list) and append:
                current[last_key].extend(new_value)
            else:
                current[last_key] = new_value
        elif create_if_missing:
            current[last_key] = new_value if not append else [new_value]
        else:
            raise KeyError(f"Key '{last_key}' not found in the dictionary.")
    elif isinstance(current, list) and isinstance(last_key, int):
        while len(current) <= last_key:
            current.append(None)
        current[last_key] = new_value
    else:
        raise TypeError("Final element must be a dict or list.")

    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

    print(f"Successfully modified '{path[-1]}' with new value.")

# Function to generate a new practice test
def generate_practice_test(file_path, practice_name):
    """
    Creates a new practice test entry and saves it to the JSON file.
    """
    # Ensure the 'practice_test' list exists
    open_and_modify(file_path, ['practice_test'], [], create_if_missing=True)

    new_practice_test = {
        'name': practice_name,
        'module_1': [],
        'module_2': [],
        'module_3': [],
        'module_4': []
    }

    # Append the new practice test to the list
    open_and_modify(file_path, ['practice_test'], [new_practice_test], append=True)

# Function to safely access the last practice test
def get_last_practice_test_index(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return len(data.get('practice_test', [])) - 1  # Return -1 if list is empty

# Main logic to generate and populate practice tests
def populate_practice_test(file_path, practice_name, num_questions):
    """
    Populates the modules of a practice test with questions based on the section and domain.
    """
    # Ensure a new practice test exists
    generate_practice_test(file_path, practice_name)

    # Get the index of the last practice test
    last_practice_test_index = get_last_practice_test_index(file_path)

    # Loop to collect and distribute questions across modules
    for i in range(1, num_questions + 1):
        if 1 <= i < 15:
            open_and_modify(
                file_path, ['practice_test', last_practice_test_index, 'module_1'],
                question_collecter('english', 'Information and Ideas', 1), append=True
            )
        elif 15 <= i < 29:
            open_and_modify(
                file_path, ['practice_test', last_practice_test_index, 'module_2'],
                question_collecter('english', 'Information and Ideas', 1), append=True
            )
        elif 29 <= i < 41:
            open_and_modify(
                file_path, ['practice_test', last_practice_test_index, 'module_3'],
                question_collecter('english', 'Information and Ideas', 1), append=True
            )
        elif 41 <= i <= 54:
            open_and_modify(
                file_path, ['practice_test', last_practice_test_index, 'module_4'],
                question_collecter('english', 'Information and Ideas', 1), append=True
            )

# Example usage
file_path = 'data.json'

# Create two practice tests and populate them with questions
populate_practice_test(file_path, 'practice test name', 54)
populate_practice_test(file_path, 'practice test name2', 54)
