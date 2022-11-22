#!/usr/bin/env python

from window.custom_window import sg
from window.custom_window import CustomWindow
from configure.configure import *
from commands.commands import Commands


class Mainrunner:

    def __init__(self):
        self.custom_window = CustomWindow()
        self.window = self.custom_window.make_window(sg.theme())

    def main(self):

        while True:
            event, values = self.window.read(timeout=100)

            # if event == sg.TIMEOUT:
            #     process = Commands.run('kubectl top node/pod')
            #     Commands.print_output(process)
            if event == sg.WIN_CLOSED:
                break
            elif event == '-GET-':
                self.custom_window.update_output(self.window, '-OUTPUT-', '')

                # =========================================================
                # values['-RESOURCES MENU-'] -> pods | deployments etc.
                # metadata -> what to apply get
                # final example `kubectl get pods`
                # =========================================================

                metadata = self.window[event].metadata
                returned_resources = Commands.run_command(metadata, values['-RESOURCES MENU-'].lower())
                self.custom_window.update_window(self.window, '-INNER RESOURCES-', returned_resources)
            elif event in ['-DESCRIBE-', '-EDIT-', '-DELETE-']:
                self.custom_window.update_output(self.window, '-OUTPUT-', '')

                # ====================================================================
                # values['-RESOURCES MENU-'] -> pods | deployments etc.
                # metadata -> what to apply, here delete | describe | edit
                # to -> values['-RESOURCES MENU-'], selected dropdown resource name
                #       - pod name
                #       - deployment name
                #       - etc
                # final example `kubectl delete pods <pod name>`
                # ====================================================================

                metadata = self.window[event].metadata
                category = values['-RESOURCES MENU-']
                Commands.run_command(f'{metadata} {category}', values['-INNER RESOURCES-'])
            elif event == '-LOGS-':
                self.custom_window.update_output(self.window, '-OUTPUT-', '')

                # ===========================================
                # values['-INNER RESOURCES-'] -> pod name
                # metadata -> what to apply, here `logs -f`
                # final example `kubectl logs -f <pod name>`
                # ===========================================

                metadata = self.window[event].metadata
                Commands.run_command(metadata, values['-INNER RESOURCES-'])
            elif event == '-KUBE FOLDER-':
                self.custom_window.update_output(self.window, '-OUTPUT-', '')

                self.window['-OUTPUT-'].update('')
                configs = configure_kube(self.window, values)
                self.custom_window.update_window(self.window, '-CONFIGURATIONS-', configs)

        self.window.close()
        exit(0)


if __name__ == '__main__':
    sg.theme('black')
    main_runner = Mainrunner()
    main_runner.main()
