# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytest_terraform']

package_data = \
{'': ['*']}

install_requires = \
['pytest>=5.3.5,<5.4.0']

entry_points = \
{'pytest11': ['terraform = pytest_terraform.plugin']}

setup_kwargs = {
    'name': 'pytest-terraform',
    'version': '0.1.0',
    'description': 'A pytest plugin for using terraform fixtures',
    'long_description': "# Introduction\n\npytest_terraform is a pytest plugin that enables executing terraform\nto provision infrastructure in a unit/functional test as a fixture.\n\nThis plugin features uses a fixture factory pattern to enable dynamic\nconstruction of fixtures as either as test decorators or module level\nvariables.\n\n\n## Philosophy\n\nThe usage/philosophy of this plugin is based on using flight recording\nfor unit tests against cloud infrastructure. In flight recording rather\nthan mocking or stubbing infrastructure, actual resources are created\nand interacted with with responses recorded, with those responses\nsubsequently replayed for fast test execution. Beyond the fidelity\noffered, this also enables these tests to be executed/re-recorded against\nlive infrastructure for additional functional/release testing.\n\n\n## Decorator Usage\n\n```python\nfrom pytest_terraform import terraform\nfrom boto3 import Session\n\n@terraform('aws_sqs')\ndef test_sqs(aws_sqs):\n   queue_url = aws_sqs['test_queue.queue_url']\n   print(queue_url)\n\n\ndef test_sqs_deliver(aws_sqs):\n   # once a fixture has been defined with a decorator\n   # it can be reused in the same module by name\n   pass\n\n@terraform('aws_sqs')\ndef test_sqs_dlq(aws_sqs):\n   # or referenced again via decorator, if redefined\n   # with decorator the fixture parameters much match.\n   pass\n```\n\n*Note* the fixture name should match the terraform module name.\n\n## Variable Usage\n\n```python\nfrom pytest_terraform import terraform\n\ngcp_pub_sub = terraform.fixture('gcp_pub_sub')\n\ndef test_queue(gcp_pub_sub):\n\tprint(gcp_pub_sub.resources)\n```\n\n*Note* the fixture variable name should match the terraform module name.\n\n## Fixture Usage\n\nThe pytest fixtures have access to everything within the terraform\nstate file, with some helpers.\n\n```\ndef test_\n\n```\n\n*Note* The terraform state file is considered an internal\nimplementation detail of terraform, not a stable interface. Also\n\n\n## Fixture support\n\n- This plugin supports all the standard pytest scopes, scope names can\n  be passed into the constructors.\n\n- It does not currently support parameterization of terraform fixtures,\n  although test functions can freely usee both.\n\n## Replay Support\n\nBy default fixtures will save a `tf_resources.json` back to the module\ndirectory, that will be used when in replay mode.\n\n## Rewriting recorded\n\nTODO\n\n## XDist Compatibility\n\npytest_terraform supports pytest-xdist in multi-process (not distributed)\nmode\n\nWhen run with python-xdist, pytest_terraform treats all non functional\nscopes as per test run fixtures across all workers, honoring their\noriginal scope lifecycle but with global semantics, instead of once\nper worker. ie. terraform non function scope fixtures are run once\nper test run, not per worker.\n\nThis in contrast to what regular fixtures do by default with\npytest-xdist, where they are executed at least once per worker. for\ninfrastructure thats potentially time instensive to setup, this can\nnegate some of the benefits of running tests in parallel, which is\nwhy pytest-terraform uses global semantics.\n\n\n### Fixture Resources\n\nthe tests will need to access fixture provisioned resources, to do so\nthe fixture will return a terraform resources instance for each\nterraform root module fixture which will have available a mapping of\nterraform resource type names to terraform resource names to provider\nids, which will be inferred from the tfstate.json.\n\n### Replay support\n\nFor tests executing with replay we'll need to store the fixture\nresource id mapping and serialize them to disk from a live\nprovisioning run to enable a replay run. On replay we'll pick up the\nserialized resource ids and return them as the fixture results. We'll\nneed to do this once per scope instantiation (session, module,\npackage, function). Note this will be effectively be an independent\nmechanism from the existing one as it needs to handled pre test\nexecution, where as the current record/replay mechanism is done within\na test execution. Some of the DRY violation could be addressed by\nrefactoring the existing mechanisms to look at fixture decorated\nattribute on the test instance.\n\nConfiguring record vs replay\n\n```\n--tf-record=false|no\n--tf-replay=yes\n```\n\n### Root module references\n\n`terraform_remote_state` can be used to introduce a dependency between\na scoped root modules on an individual test, note we are not\nattempting to support same scope inter fixture dependencies as that\nimposes additional scheduling constraints outside of pytest native\ncapabilities. The higher scoped root module will need to have output\nvariables to enable this consumption.\n\n\n\n",
    'author': 'Kapil Thangavelu',
    'author_email': 'kapilt@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/cloud-custodian/pytest-terraform',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
