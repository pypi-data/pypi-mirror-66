from ..util.bovy_conversion import physical_compatible
_APY_LOADED= True
try:
    from astropy import units
except ImportError:
    _APY_LOADED= False
from ..util import config
class df(object):
    """Top-level class for DF classes"""
    def __init__(self,ro=None,vo=None):
        """
        NAME:
           __init__
        PURPOSE:
           initialize a DF object
        INPUT:
           ro= (None) distance scale
           vo= (None) velocity scale
        OUTPUT:
        HISTORY:
           2016-02-28 - Written - Bovy (UofT)
        """
        # Parse ro and vo
        if ro is None:
            self._ro= config.__config__.getfloat('normalization','ro')
            self._roSet= False
        else:
            if _APY_LOADED and isinstance(ro,units.Quantity):
                ro= ro.to(units.kpc).value
            self._ro= ro
            self._roSet= True
        if vo is None:
            self._vo= config.__config__.getfloat('normalization','vo')
            self._voSet= False
        else:
            if _APY_LOADED and isinstance(vo,units.Quantity):
                vo= vo.to(units.km/units.s).value
            self._vo= vo
            self._voSet= True
        return None

    def _check_consistent_units(self):
        """Internal function to check that the set of units for this object is consistent with that for the potential"""
        assert physical_compatible(self,self._pot),  'Physical conversion for the DF object is not consistent with that of the Potential given to it'
            
    def turn_physical_off(self):
        """
        NAME:

           turn_physical_off

        PURPOSE:

           turn off automatic returning of outputs in physical units

        INPUT:

           (none)

        OUTPUT:

           (none)

        HISTORY:

           2017-06-05 - Written - Bovy (UofT)

        """
        self._roSet= False
        self._voSet= False
        return None

    def turn_physical_on(self,ro=None,vo=None):
        """
        NAME:

           turn_physical_on

        PURPOSE:

           turn on automatic returning of outputs in physical units

        INPUT:

           ro= reference distance (kpc; can be Quantity)

           vo= reference velocity (km/s; can be Quantity)

        OUTPUT:

           (none)

        HISTORY:

           2016-06-05 - Written - Bovy (UofT)

           2020-04-22 - Don't turn on a parameter when it is False - Bovy (UofT)

        """
        if not ro is False: self._roSet= True
        if not vo is False: self._voSet= True
        if not ro is None and ro:
            if _APY_LOADED and isinstance(ro,units.Quantity):
                ro= ro.to(units.kpc).value
            self._ro= ro
        if not vo is None and vo:
            if _APY_LOADED and isinstance(vo,units.Quantity):
                vo= vo.to(units.km/units.s).value
            self._vo= vo
        return None  
