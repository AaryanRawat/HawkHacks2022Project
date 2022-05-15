"""
Reads data from a .env file with the following format:
    Lines of format: var_name=value
    All variables are on separate lines
    Lines starting with '#' are ignored
    No empty lines
Data is returned in the ENV dictionary object
"""

def get_env_data_as_dict(path: str) -> dict:
    with open(path, 'r') as f:
       return dict(tuple(line.replace('\n', '').split('=')) for line
                in f.readlines() if not line.startswith('#'))

ENV = get_env_data_as_dict('.env')

