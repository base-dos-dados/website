import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckan.plugins.toolkit import get_action
import collections
import pprint
import types


class BasedosdadosPlugin(
    plugins.SingletonPlugin,
):  # toolkit.DefaultDatasetForm):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.interfaces.IFacets)
    plugins.implements(plugins.interfaces.ITemplateHelpers)
    plugins.implements(plugins.IValidators)
    plugins.implements(plugins.IActions)
    plugins.implements(plugins.IPackageController, inherit=True)
    # plugins.implements(plugins.IDatasetForm)

    # IFacets
    def dataset_facets(self, facet_dict, package_type):
        facets = collections.OrderedDict()
        # get_action('package_list')(None, {})
        # asian = get_action('package_show')(None, {'id': 'asian-barometer'})
        facets["download_type"] = "Forma de Download"
        facets["organization"] = "Organização"
        facets["groups"] = "Grupos"
        facets["tags"] = "Tags"
        # facets['pais'] = 'País'
        # facets['nivel_observacao'] = 'Nivel da Observação'
        # facets['ano'] = 'Anos'
        return facets
        # OPTIONS: dict_keys(['license_title', 'maintainer', 'relationships_as_object', 'private',
        # 'maintainer_email', 'num_tags', 'id', 'metadata_created', 'owner_org', 'metadata_modified',
        # 'author', 'author_email', 'state', 'version', 'license_id', 'type', 'resources', 'num_resources',
        # 'tags', 'groups', 'creator_user_id', 'relationships_as_subject', 'name', 'isopen', 'url', 'notes',
        # 'title', 'extras', 'license_url', 'organization'])

    def group_facets(self, facets_dict, group_type, package_type):
        return self.dataset_facets(facets_dict, package_type)

    def organization_facets(self, facets_dict, organization_type, package_type):
        return self.dataset_facets(package_type)

    # IConfigurer
    def update_config(self, config_):
        toolkit.add_template_directory(config_, "templates")
        toolkit.add_public_directory(config_, "public")
        toolkit.add_public_directory(config_, "assets")
        # toolkit.add_resource('fanstatic', 'basedosdados')
        toolkit.add_resource("assets", "basedosdados")

    def get_helpers(self):
        import boltons.strutils
        import ckanext.basedosdados.template_functions as template_functions

        funs = _read_functions_from_module(template_functions)
        funs["boltons"] = boltons
        return funs

    # IValidators
    def get_validators(self):
        import ckanext.basedosdados.validator_functions as validators

        return _read_functions_from_module(validators)

    # IActions
    def get_actions(self):
        import ckanext.basedosdados.endpoint_functions as endpoints

        return _read_functions_from_module(endpoints)

    # IPackageController
    # def before_index(self, data_dict):
    #     name = []
    #     description = []
    #     for col in data_dict.get("columns", []):
    #         name.append(col["name"])
    #         description.append(col["description"])
    #     data_dict["name"] = "\n".join(name)
    #     data_dict["description"] = "\n".join(description)


def _read_functions_from_module(module):
    funs = {
        name: getattr(module, name) for name in dir(module) if not name.startswith("_")
    }
    funs = {k: v for k, v in funs.items() if isinstance(v, types.FunctionType)}
    return funs
