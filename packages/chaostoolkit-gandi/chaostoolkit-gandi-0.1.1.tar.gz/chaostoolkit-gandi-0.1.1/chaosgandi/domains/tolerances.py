from typing import Any, Dict, List

from chaoslib.exceptions import ActivityFailed
from dateparser import parse
from logzero import logger

__all__ = ["domains_should_not_expire_in"]
TZ_SETTINGS = {'TIMEZONE': 'UTC', 'RETURN_AS_TIMEZONE_AWARE': True}


def domains_should_not_expire_in(value: List[Dict[str, Any]] = None,
                                 when: str = '1 month'):
    """
    Go through the list of Gandi domains and fails if any expires before
    the given date treshold as a relative time to now.
    """
    no_sooner_than_date = parse(
        'in {}'.format(when), settings=TZ_SETTINGS)
    if not no_sooner_than_date:
        raise ActivityFailed(
            "Failed to parse `when` date '{}' for Gandi domain expire "
            "tolerance".format(when))

    logger.debug(
        "Looking through domains to see if any expires before '{}'".format(
            no_sooner_than_date))
    for domain in value:
        expire_date = parse(
            domain["dates"]["registry_ends_at"], settings=TZ_SETTINGS)
        if expire_date < no_sooner_than_date:
            logger.warning(
                "Domain '{}' expires in less than '{}': {}".format(
                    domain["fqdn_unicode"], when,
                    domain["dates"]["registry_ends_at"]))
            raise ActivityFailed()


def domain_nameservers_should_contain(value: List[str] = None,
                                      ns: str = None) -> bool:
    """
    Check the given nameserver is in the given domain's nameservers.
    """
    return ns in value


def domain_nameservers_should_not_contain(value: List[str], ns: str) -> bool:
    """
    Check the given nameserver is not in the given domain's nameservers.
    """
    return ns not in value


def domain_nameservers_should_be_a_subset_of(value: List[str] = None,
                                             ns: List[str] = None) -> bool:
    """
    Check the given nameservers are a subset of the domain's nameservers.
    """
    return set(ns).issubset(value)


def domain_nameservers_should_be_a_superset_of(value: List[str] = None,
                                               ns: List[str] = None) -> bool:
    """
    Check the given nameservers are a superset of the domain's nameservers.
    """
    return set(ns).issuperset(value)


def domain_nameservers_should_be_exactly(value: List[str] = None,
                                         ns: List[str] = None) -> bool:
    """
    Check the given nameservers are exactly the domain's nameservers.
    """
    return set(value) == set(ns)
