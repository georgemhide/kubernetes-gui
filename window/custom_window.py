import PySimpleGUI as sg


class CustomWindow:

    def __int__(self):
        pass

    @staticmethod
    def update_window(window, key, values):
        window[key].update(values=values)

    @staticmethod
    def update_output(window, key, value):
        window[key].update(value)

    @staticmethod
    def make_window(theme):
        sg.theme(theme)
        # wrapper for all subparts
        layout = []

        # row for setting up the configuration
        configuration_row = [
            [
                # Locate and set your .kube folder here
                sg.Text("Find .kube =>"),
                sg.In(size=(25, 1), enable_events=True, key="-KUBE FOLDER-"),
                sg.FolderBrowse(enable_events=True),
                sg.VSeparator(),
                # Locate and set your config options
                sg.OptionMenu(
                    size=(10, 1),
                    values=[''],
                    default_value='Namespace',
                    key='-CONFIGURATIONS-',
                    tooltip='Select config file and set appropriate namespace'
                ),
            ],
            [
                sg.HSeparator()
            ]
        ]

        # column of list options
        options_list = [
            [
                sg.OptionMenu(
                    values=('Deployments',
                            'Pods',
                            'Secrets',
                            'ConfigMaps',
                            'Services',
                            'ServiceEntries',
                            'ReplicaSets'),
                    default_value='Applications',
                    key='-RESOURCES MENU-',
                    tooltip='Select application that you want to see for selected namespace'
                ),
                sg.VSeparator(),
                sg.Button('Get',
                          enable_events=True,
                          key='-GET-',
                          metadata='get'),
                sg.VSeparator(),
                sg.OptionMenu(
                    values=[''],
                    size=(25, 1),
                    default_value='Resource Name',
                    key='-INNER RESOURCES-',
                    tooltip='Select something'
                ),
                sg.VSeparator(),
                sg.Button('Logs',
                          enable_events=True,
                          key='-LOGS-',
                          metadata='logs -f'),
                sg.Button('Edit',
                          enable_events=True,
                          key='-EDIT-',
                          metadata='edit'),
                sg.Button('Describe',
                          enable_events=True,
                          key='-DESCRIBE-',
                          metadata='describe'),
                sg.Button('Delete',
                          enable_events=True,
                          key='-DELETE-',
                          metadata='delete')
            ],
            [
                sg.HSeparator()
            ]
        ]

        logging_layout = [
            [sg.Text("Anything printed will display here!")],
            [sg.Multiline(size=(60, 15),
                          font='Courier 8',
                          expand_x=True,
                          expand_y=True,
                          write_only=True,
                          reroute_stdout=True,
                          reroute_stderr=True,
                          echo_stdout_stderr=True,
                          autoscroll=True,
                          auto_refresh=True,
                          key='-OUTPUT-')]
        ]

        layout.append([
            configuration_row,
            options_list,
            logging_layout
        ])

        window = sg.Window(title="A GUI for kubernetes?",
                           layout=layout,
                           size=('860', '640'),
                           right_click_menu_tearoff=True,
                           grab_anywhere=True,
                           resizable=True,
                           margins=(0, 0),
                           use_custom_titlebar=True,
                           finalize=True,
                           keep_on_top=True)

        window.set_min_size(window.size)

        return window
