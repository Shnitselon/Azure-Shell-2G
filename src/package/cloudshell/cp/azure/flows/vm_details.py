import jsonpickle

from package.cloudshell.cp.azure.actions.vm import VMActions
from package.cloudshell.cp.azure.actions.vm_details import VMDetailsActions


class AzureGetVMDetailsFlow:
    def __init__(self, resource_config, azure_client, cancellation_manager, reservation_info, logger):
        """

        :param resource_config:
        :param azure_client:
        :param cancellation_manager:
        :param reservation_info:
        :param logging.Logger logger:
        """
        self._resource_config = resource_config
        self._azure_client = azure_client
        self._cancellation_manager = cancellation_manager
        self._reservation_info = reservation_info
        self._logger = logger

    def get_vm_details(self, request_actions):
        """

        :param request_actions:
        :return:
        """
        resource_group_name = self._reservation_info.get_resource_group_name()

        vm_actions = VMActions(azure_client=self._azure_client, logger=self._logger)
        vm_details_actions = VMDetailsActions(azure_client=self._azure_client, logger=self._logger)

        results = []

        for deployed_app in request_actions.deployed_apps:
            with self._cancellation_manager:
                vm = vm_actions.get_vm(vm_name=deployed_app.name, resource_group_name=resource_group_name)

                # todo: override deployed_app model instead?????
                if deployed_app.deployment_service_model == "Microsoft Azure 2G.Azure VM From Marketplace 2G":
                    result = vm_details_actions.prepare_marketplace_vm_details(virtual_machine=vm,
                                                                               resource_group_name=resource_group_name)
                else:
                    result = vm_details_actions.prepare_custom_vm_details(virtual_machine=vm,
                                                                          resource_group_name=resource_group_name)
                results.append(result)

        return self.prepare_command_result(results)

    # todo: add base class with this function to the cloudshell-cp-core package
    def prepare_command_result(self, result):
        """Serializes output as JSON and writes it to console output wrapped with special prefix and suffix

        :param result: Result to return
        """
        return jsonpickle.encode(result)
