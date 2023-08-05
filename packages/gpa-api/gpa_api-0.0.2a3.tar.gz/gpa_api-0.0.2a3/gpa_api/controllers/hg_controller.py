import connexion
import six

from gpa_api.models.hg_fluid import HgFluid  # noqa: E501
from gpa_api import util


def create_fluid(hg_fluid):  # noqa: E501
    """Create hg fluid

     # noqa: E501

    :param hg_fluid: 
    :type hg_fluid: dict | bytes

    :rtype: HgFluid
    """
    if connexion.request.is_json:
        hg_fluid = HgFluid.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def get_fluid(fluid_id):  # noqa: E501
    """Get fluid

     # noqa: E501

    :param fluid_id: The id of the fluid
    :type fluid_id: int

    :rtype: HgFluid
    """
    return 'do some magic!'


def get_fluids():  # noqa: E501
    """Get hg fluids

     # noqa: E501


    :rtype: List[HgFluid]
    """
    return 'do some magic!'
