import requests, subprocess
import json
import base64

def download_readme(owner, repo):
    url = f'https://api.github.com/repos/{owner}/{repo}/contents/README.md'
    response = requests.get(url)
    readme_contents = response.json()['content']
    readme_contents = readme_contents.encode('ascii')
    return base64.b64decode(readme_contents).decode('utf-8')

def extract_commands(text):
    commands_list = []
    start_index = text.find('```bash\n')
    while start_index != -1:
        end_index = text.find('```', start_index + 7)  # +7 to account for the "```bash\n"
        if end_index == -1:
            break
        bash_content = text[start_index + 7:end_index]
        lines = bash_content.splitlines()

        for line in lines:
            command_parts = line.strip().split(' ', 1)
            if command_parts:
                command_name = command_parts[0]
                command_value = command_parts[1] if len(command_parts) > 1 else ''
                if command_name or command_value:  # Exclude empty commands
                    commands_list.append({'command': command_name, 'value': command_value})

        start_index = text.find('```bash\n', end_index)

    return commands_list

def main():
    owner = 'Loeffeldude'
    repo = 'my-chat-gpt'
    text = download_readme(owner, repo)
    commands_list = extract_commands(text)

    # Convert commands_list to JSON format and print the result
    json_data = json.dumps(commands_list, indent=2)
    print(json_data)
    test_run(commands_list)

def conda_activate(environment_name):
    # Perform the activation command or any other desired action here
    print(f"Activating conda environment: {environment_name}")

def execute_command(command_info):
    command_name = command_info['command']
    command_value = command_info['value']
    command = f"{command_name} {command_value}"
    try:
        print(f"Executing command: {command}")
        subprocess.run(command, shell=True, check=True, stderr=subprocess.STDOUT, text=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {command}")
        print("Error message:")
        print(e.output)

def test_run(commands_list):
    environment_name = 'Localtools'
    conda_activate(environment_name)
    for command_info in commands_list:
        execute_command(command_info)

if __name__ == "__main__":
    main()
