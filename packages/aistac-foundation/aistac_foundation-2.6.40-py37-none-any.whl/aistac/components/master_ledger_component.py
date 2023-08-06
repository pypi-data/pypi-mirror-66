from aistac.components.abstract_component import AbstractComponent
from aistac.intent.master_ledger_intent_model import MasterLedgerIntentModel
from aistac.properties.abstract_properties import AbstractPropertyManager
from aistac.properties.master_ledger_property_manager import MasterLedgerPropertyManager

__author__ = 'Darryl Oatridge'


class MasterLedger(AbstractComponent):

    def __init__(self, property_manager: MasterLedgerPropertyManager, intent_model: MasterLedgerIntentModel,
                 default_save=None, reset_templates: bool=None, align_connectors: bool=None):
        """ Encapsulation class for the transition set of classes

        :param property_manager: The contract property manager instance for this component
        :param intent_model: the model codebase containing the parameterizable intent
        :param default_save: The default behaviour of persisting the contracts:
                    if False: The connector contracts are kept in memory (useful for restricted file systems)
        :param reset_templates: (optional) reset connector templates from environ variables (see `report_environ()`)
        :param align_connectors: (optional) resets aligned connectors to the template
        """
        super().__init__(property_manager=property_manager, intent_model=intent_model, default_save=default_save,
                         reset_templates=reset_templates, align_connectors=align_connectors)

    @classmethod
    def from_uri(cls, task_name: str, uri_pm_path: str, pm_file_type: str=None, pm_module: str=None,
                 pm_handler: str=None, pm_kwargs: dict=None, default_save=None, reset_templates: bool=None,
                 align_connectors: bool=None, default_save_intent: bool=None, default_intent_level: bool=None,
                 order_next_available: bool=None, default_replace_intent: bool=None):
        """ Class Factory Method to instantiates the components application. The Factory Method handles the
        instantiation of the Properties Manager, the Intent Model and the persistence of the uploaded properties.
        See class inline docs for an example method

         :param task_name: The reference name that uniquely identifies a task or subset of the property manager
         :param uri_pm_path: A URI that identifies the resource path for the property manager.
         :param pm_file_type: (optional) defines a specific file type for the property manager
         :param pm_module: (optional) the module or package name where the handler can be found
         :param pm_handler: (optional) the handler for retrieving the resource
         :param pm_kwargs: (optional) a dictionary of kwargs to pass to the property manager
         :param default_save: (optional) if the configuration should be persisted. default to 'True'
         :param reset_templates: (optional) reset connector templates from environ variables. Default True
                                (see `report_environ()`)
         :param align_connectors: (optional) resets aligned connectors to the template. default Default True
         :param default_save_intent: (optional) The default action for saving intent in the property manager
         :param default_intent_level: (optional) the default level intent should be saved at
         :param order_next_available: (optional) if the default behaviour for the order should be next available order
         :param default_replace_intent: (optional) the default replace existing intent behaviour
         :return: the initialised class instance
         """
        pm_file_type = pm_file_type if isinstance(pm_file_type, str) else 'json'
        pm_module = pm_module if isinstance(pm_module, str) else 'aistac.handlers.python_handlers'
        pm_handler = pm_handler if isinstance(pm_handler, str) else 'PythonPersistHandler'
        _pm = MasterLedgerPropertyManager(task_name=task_name)
        _intent_model = MasterLedgerIntentModel(property_manager=_pm, default_save_intent=default_save_intent,
                                                order_next_available=order_next_available,
                                                default_intent_level=default_intent_level,
                                                default_replace_intent=default_replace_intent)
        super()._init_properties(property_manager=_pm, uri_pm_path=uri_pm_path, pm_file_type=pm_file_type,
                                 pm_module=pm_module, pm_handler=pm_handler, pm_kwargs=pm_kwargs)
        return cls(property_manager=_pm, intent_model=_intent_model, default_save=default_save,
                   reset_templates=reset_templates, align_connectors=align_connectors)

    @classmethod
    def from_env(cls, task_name: str=None, default_save=None, reset_templates: bool=None, align_connectors: bool=None,
                 default_save_intent: bool=None, default_intent_level: bool=None,  order_next_available: bool=None,
                 default_replace_intent: bool=None, **kwargs):
        """ Class Factory Method that builds the connector handlers taking the property contract path from
        the os.environ['AISTAC_PM_PATH'] or, if not found, uses the system default,
                    for Linux and IOS '/tmp/components/contracts
                    for Windows 'os.environ['AppData']\\components\\contracts'
        The following environment variables can be set:
        'AISTAC_PM_PATH': the property contract path, if not found, uses the system default
        'AISTAC_PM_TYPE': a file type for the property manager. If not found sets as 'json'
        'AISTAC_PM_MODULE': a default module package, if not set uses component default
        'AISTAC_PM_HANDLER': a default handler. if not set uses component default

        This method calls to the Factory Method 'from_uri(...)' returning the initialised class instance

         :param task_name: The reference name that uniquely identifies a task or subset of the property manager
         :param default_save: (optional) if the configuration should be persisted
         :param reset_templates: (optional) reset connector templates from environ variables. Default True
                                (see `report_environ()`)
         :param align_connectors: (optional) resets aligned connectors to the template. default Default True
         :param default_save_intent: (optional) The default action for saving intent in the property manager
         :param default_intent_level: (optional) the default level intent should be saved at
         :param order_next_available: (optional) if the default behaviour for the order should be next available order
         :param default_replace_intent: (optional) the default replace existing intent behaviour
         :param kwargs: to pass to the property ConnectorContract as its kwargs
         :return: the initialised class instance
         """
        task_name = task_name if isinstance(task_name, str) else 'ledger'
        return super().from_env(task_name=task_name, default_save=default_save, reset_templates=reset_templates,
                                align_connectors=align_connectors, default_save_intent=default_save_intent,
                                default_intent_level=default_intent_level, order_next_available=order_next_available,
                                default_replace_intent=default_replace_intent)

    @property
    def pm(self) -> MasterLedgerPropertyManager:
        return self._component_pm

    @property
    def intent_model(self) -> MasterLedgerIntentModel:
        return self._intent_model

    @property
    def ledger_catalog(self) -> dict:
        """returns a dictionary of managers and their tasks"""
        return self.pm.ledger_catalog

    def add_ledger_pm(self, property_manager: AbstractPropertyManager, save: bool=None):
        """ adds a pm to the ledger

        :param property_manager: the instance of the property manager to add
        :param save: (optional) override of the default save action set at initialisation.
       """
        save = save if isinstance(save, bool) else self._default_save
        self.pm.set_ledger_pm(property_manager)
        self.pm_persist(save)

    def remove_ledger_pm(self, manager: str, task: str, save: bool=None):
        """ removes a pm from the ledger

        :param manager: The name of the component manager
        :param task: The name of the manager task
        :param save: (optional) override of the default save action set at initialisation.
        :return True if removed, False if not
        """
        save = save if isinstance(save, bool) else self._default_save
        result = self.pm.remove_ledger_pm(manager=manager, task=task)
        self.pm_persist(save)
        return result

    def report_tasks(self, manager_filter: [list, str]=None):
        """"""
        self.pm.report_ledger(manager_filter=manager_filter)
