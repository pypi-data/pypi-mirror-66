from typing import Any, Dict, List
from urllib.parse import urlencode

from chaoslib.exceptions import ActivityFailed
from chaoslib.types import Configuration, Secrets
from logzero import logger

from chaosgandi import gandi_client, gandi_url

__all__ = ["list_domains", "list_nameservers"]


def list_domains(fqdn_filter: str = None, tld_filter: str = None,
                 configuration: Configuration = None,
                 secrets: Secrets = None) -> List[Dict[str, Any]]:
    """
    List all domains or those matching the given TLD or FQDN filters and
    return the list as-is.

    See https://api.gandi.net/docs/domains/#v5-domain-domains
    """
    with gandi_client(configuration, secrets) as client:
        url = gandi_url("/v5/domain/domains")

        qs = {}
        if fqdn_filter:
            qs["fqdn"] = fqdn_filter
        if tld_filter:
            qs["tld"] = tld_filter

        if qs:
            url = "{}?{}".format(url, urlencode(qs))

        r = client.get(url)
        if r.status_code > 399:
            raise ActivityFailed(
                "Failed to list domains from Gandi: {}".format(r.text))
        domains = r.json()
        logger.debug("Gandi domains: {}".format(domains))
        return domains


def list_nameservers(domain: str, configuration: Configuration = None,
                     secrets: Secrets = None) -> List[str]:
    """
    List nameservers set for this domain and return them as a list of strings.

    See https://api.gandi.net/docs/domains/#v5-domain-domains-domain-nameservers
    """  # noqa: E501
    with gandi_client(configuration, secrets) as client:
        url = gandi_url("/v5/domain/domains/{}/nameservers".format(domain))
        r = client.get(url)
        if r.status_code > 399:
            raise ActivityFailed(
                "Failed to list nameservers from Gandi: {}".format(r.text))
        ns = r.json()
        logger.debug("Gandi nameservers for {}: {}".format(domain, ns))
        return ns
