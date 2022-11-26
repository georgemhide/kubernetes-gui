class Utils:
    def __init__(self, consts):
        self.consts = consts

    def handle_response(self, response):
        if response.status_code != 200:
            print(f"Response Code: {response.status_code} with message: {response.json()['message']}")
        return response

    def get_namespace(self, values):
        if values[self.consts.namespaces] != '':
            return f'/namespaces/{values[self.consts.namespaces]}'
        return ''

    # This method can be moved to a util file
    def parse_items_for_name(self, data):
        pods = []
        for item in data:
            pods.append(item['metadata']['name'])
        return pods

    def pretty_print_resource(self, data, resource_type):
        to_print = ""
        if len(data) == 0:
            to_print = f'Found nothing for {resource_type}'

        for item in data:
            to_print += \
                f"""
    Resource : {resource_type}
    #===============================================================================================================#
    {item['metadata']['name']} {self.get_extra_data(item, resource_type)}
    #===============================================================================================================#
    """
        print(to_print)

    def get_extra_data(self, item, resource_type):
        if resource_type == 'Pods':
            return f"""| {item['status']['phase']} | Containers ({len(item['spec']['containers'])})
    {self.prepare_container(item)}"""
        return ''

    def prepare_container(self, item):
        for container in item['spec']['containers']:
            status = self.prepare_container_status(container['name'], item['status']['containerStatuses'])
            return f"C.Name: {container['name']} | {status}"

    def prepare_container_status(self, container, container_statuses):
        for container_status in container_statuses:
            if container_status['name'] == container:
                return f"Ready/Started: {container_status['ready']}/{container_status['started']} | " \
                       f"Restarts: {container_status['restartCount']} "
