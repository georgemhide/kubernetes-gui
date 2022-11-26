#!/usr/bin/env python
from utils.utils import Utils
from window.custom_window import sg
from window.custom_window import CustomWindow
from commands.commands import Commands
from constants.consts import Consts


class Mainrunner:

    def __init__(self):
        self.consts = Consts()
        self.utils = Utils(self.consts)
        self.custom_window = CustomWindow(self.consts)
        self.window = self.custom_window.make_window(sg.theme())
        self.commands = Commands()

    def main(self):
        namespace_response = self.utils.handle_response(self.commands.run_api_command_get('/namespaces'))
        if namespace_response.status_code == 200:
            self.custom_window.update_window(self.window,
                                             self.consts.namespaces,
                                             self.utils.parse_items_for_name(namespace_response.json()['items']))

        while True:
            event, values = self.window.read(timeout=100)

            if event == sg.WIN_CLOSED:
                break
            # =========================================================
            # values[self.consts.resources_menu] -> pods | deployments etc.
            # makes a get request to kubernetes api to get the required resource
            # =========================================================
            elif event == self.consts.get:
                self.custom_window.update_output(self.window, self.consts.output, '')

                response = self.utils.handle_response(
                    self.commands.run_api_command_get(f'{self.utils.get_namespace(values)}'
                                                      f'/{values[self.consts.resources_menu].lower()}'))

                if response.status_code == 200:
                    response_data = response.json()['items']
                    resource_names = self.utils.parse_items_for_name(response_data)

                    self.utils.pretty_print_resource(response_data, values[self.consts.resources_menu])

                    self.custom_window.update_window(self.window, self.consts.inner_resources, resource_names)
            elif event == self.consts.delete:
                delete_resource = self.commands.delete_resource(f'{self.utils.get_namespace(values)}'
                                                                f'/{values[self.consts.resources_menu].lower()}'
                                                                f'/{values[self.consts.inner_resources]}')
                if delete_resource.status_code == 200:
                    print(f'Deleted {values[self.consts.inner_resources]}')
                else:
                    print(f'{delete_resource.content}')
            # ====================================================================
            # values[self.consts.resources_menu] -> pods | deployments etc.
            # metadata -> what to apply, here delete | describe | edit
            # to -> values[self.consts.resources_menu], selected dropdown resource name
            #       - pod name
            #       - deployment name
            #       - etc
            # final example `kubectl delete pods <pod name>`
            # ====================================================================
            elif event in [self.consts.describe, self.consts.edit]:
                self.custom_window.update_output(self.window, self.consts.output, '')
                metadata = self.window[event].metadata
                category = values[self.consts.resources_menu]
                self.commands.run_command(f'{metadata} {category}', values[self.consts.inner_resources])
            # ===========================================
            # values[self.consts.inner_resources] -> pod name
            # metadata -> what to apply, here `logs -f`
            # final example `kubectl logs -f <pod name>`
            # ===========================================
            elif event == self.consts.logs:
                self.custom_window.update_output(self.window, self.consts.output, '')
                metadata = self.window[event].metadata
                self.commands.run_command(metadata, values[self.consts.inner_resources])
            elif event == self.consts.kube_folder:
                pass
                # self.custom_window.update_output(self.window, self.consts.output, '')

                # self.window[self.consts.output].update('')
                # configs = configure_kube(self.window, values)
                # self.custom_window.update_window(self.window, '-CONFIGURATIONS-', configs)

        self.window.close()
        exit(0)


if __name__ == '__main__':
    sg.theme('black')
    main_runner = Mainrunner()
    main_runner.main()
