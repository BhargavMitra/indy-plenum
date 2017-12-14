import importlib

import pytest

from plenum import setup_plugins, PLUGIN_LEDGER_IDS, PLUGIN_CLIENT_REQUEST_FIELDS
from plenum.common.pkg_util import update_module_vars
from plenum.test.plugin.demo_plugin.main import update_node_obj

from plenum.test.pool_transactions.conftest import clientAndWallet1, \
    client1, wallet1, client1Connected, looper, stewardAndWallet1, \
    stewardWallet, steward1


@pytest.fixture(scope="module")
def tconf(tconf, request):
    global PLUGIN_LEDGER_IDS, PLUGIN_CLIENT_REQUEST_FIELDS

    orig_plugin_root = tconf.PLUGIN_ROOT
    orig_enabled_plugins = tconf.ENABLED_PLUGINS
    orig_plugin_ledger_ids = PLUGIN_LEDGER_IDS
    orig_plugin_client_req_fields = PLUGIN_CLIENT_REQUEST_FIELDS

    update_module_vars('plenum.config',
                       **{
                           'PLUGIN_ROOT': 'plenum.test.plugin',
                           'ENABLED_PLUGINS': ['demo_plugin', ],
                       })
    PLUGIN_LEDGER_IDS = set()
    PLUGIN_CLIENT_REQUEST_FIELDS = {}
    setup_plugins()

    # The next imports and reloading are needed only in tests, since in
    # production none of these modules would be loaded before plugins are
    # setup (not initialised)
    import plenum.server

    importlib.reload(plenum.server.replica)
    importlib.reload(plenum.server.node)
    importlib.reload(plenum.server.view_change.view_changer)

    def reset():
        global PLUGIN_LEDGER_IDS, PLUGIN_CLIENT_REQUEST_FIELDS
        update_module_vars('plenum.config',
                           **{
                               'PLUGIN_ROOT': orig_plugin_root,
                               'ENABLED_PLUGINS': orig_enabled_plugins,
                           })
        PLUGIN_LEDGER_IDS = orig_plugin_ledger_ids
        PLUGIN_CLIENT_REQUEST_FIELDS = orig_plugin_client_req_fields
        setup_plugins()

    request.addfinalizer(reset)
    return tconf


@pytest.fixture(scope="module")
def txnPoolNodeSet(txnPoolNodeSet):
    for node in txnPoolNodeSet:
        update_node_obj(node)
    return txnPoolNodeSet