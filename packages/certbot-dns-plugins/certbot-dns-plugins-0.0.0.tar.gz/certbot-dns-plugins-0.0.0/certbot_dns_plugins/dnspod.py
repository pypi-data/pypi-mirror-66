import logging

import zope.interface
from certbot import interfaces
from certbot.plugins import dns_common
from dnspod_sdk import DnspodClient

from . import __version__ as dnspod_client_version

logger = logging.getLogger(__name__)


@zope.interface.implementer(interfaces.IAuthenticator)
@zope.interface.provider(interfaces.IPluginFactory)
class Authenticator(dns_common.DNSAuthenticator):
    """DNS Authenticator for Cloudflare

    This Authenticator uses the Cloudflare API to fulfill a dns-01 challenge.
    """

    description = "使用DNS TXT记录获取证书（如果使用DNSPod管理DNS）"

    def __init__(self, *args, **kwargs):
        super(Authenticator, self).__init__(*args, **kwargs)
        self.credentials = None

    @classmethod
    def add_parser_arguments(cls, add):  # pylint: disable=arguments-differ
        super(Authenticator, cls).add_parser_arguments(add)
        add("credentials", help="DNSPod credentials INI file.")

    def more_info(self):  # pylint: disable=missing-function-docstring
        return "This plugin configures a DNS TXT record to respond to a dns-01 challenge using " + "the DNSPod API."

    def _setup_credentials(self):
        self.credentials = self._configure_credentials(
            "credentials",
            "DNSPod credentials INI file",
            {"token_id": "API token_id for DNSPod account", "token": "API token for DNSPod account"},
        )

    def _perform(self, domain, validation_name, validation):
        self._get_dnspod_client().add_txt_record(domain, validation_name, validation)

    def _cleanup(self, domain, validation_name, validation):
        self._get_dnspod_client().del_txt_record(domain, validation_name, validation)

    def _get_dnspod_client(self):
        return _DNSPodClient(self.credentials.conf("token_id"), self.credentials.conf("token"))


class _DNSPodClient(object):
    """
    Encapsulates all communication with the DNSPod API.
    """

    def __init__(self, token_id, token):
        user_agent = f"Certbot DNS Pod/{dnspod_client_version}(me@codeif.com))"
        print("this is user_agent", user_agent)
        self.dc = DnspodClient(token_id, token, user_agent)

    def add_txt_record(self, domain_name, record_name, record_content):
        """
        Add a TXT record using the supplied information.

        :param str domain_name: The domain to use to associate the record with.
        :param str record_name: The record name (typically beginning with '_acme-challenge.').
        :param str record_content: The record content (typically the challenge validation).
        :raises certbot.errors.PluginError: if an error occurs communicating with the DNSPod API
        """
        pass

    def del_txt_record(self, domain_name, record_name, record_content):
        """
        Delete a TXT record using the supplied information.

        Note that both the record's name and content are used to ensure that similar records
        created concurrently (e.g., due to concurrent invocations of this plugin) are not deleted.

        Failures are logged, but not raised.

        :param str domain_name: The domain to use to associate the record with.
        :param str record_name: The record name (typically beginning with '_acme-challenge.').
        :param str record_content: The record content (typically the challenge validation).
        """
        pass

    def _find_domain(self, domain_name):
        """
        Find the domain object for a given domain name.

        :param str domain_name: The domain name for which to find the corresponding Domain.
        :returns: The Domain, if found.
        :rtype: `~dnspod.Domain`
        :raises certbot.errors.PluginError: if no matching Domain is found.
        """
        pass
