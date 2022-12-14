import subprocess
import requests


class Commands:

    def __init__(self):
        self.base_url = 'http://127.0.0.1:8080/api/v1'
        pass

    @staticmethod
    def prepare_command(what_to_do, where_to_do):
        return f'kubectl {what_to_do} {where_to_do}'

    def run_api_command_get(self, uri):
        response = requests.get(f'{self.base_url}{uri}')
        return response

    def delete_resource(self, uri):
        response = requests.delete(f'{self.base_url}{uri}')
        return response

    @staticmethod
    def run_command(what_to_do, where_to_do):
        command = Commands.prepare_command(what_to_do, where_to_do)
        process = Commands.run(command)
        r = []

        while True:
            # Do something else
            return_code = process.poll()
            if return_code is not None:
                counter = 0
                # Process has finished, read rest of the output
                for output in process.stdout.readlines():
                    counter += 1
                    striped_output = output.strip()
                    print(striped_output)
                    if counter > 1:
                        keep = striped_output.split(' ')[0]
                        r.append(keep)

                break

        return r

    @staticmethod
    def run(command):
        process = subprocess.Popen(command,
                                   stdout=subprocess.PIPE,
                                   universal_newlines=True,
                                   shell=True,
                                   text=True)
        return process

    @staticmethod
    def print_output(process):
        while True:
            return_code = process.poll()
            if return_code is not None:
                # Process has finished, read rest of the output
                for output in process.stdout.readlines():
                    print(output.strip())
                break
