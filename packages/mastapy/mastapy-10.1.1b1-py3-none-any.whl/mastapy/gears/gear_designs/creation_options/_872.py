﻿'''_872.py

HypoidGearSetCreationOptions
'''


from mastapy.gears.gear_designs.creation_options import _871
from mastapy.gears.gear_designs.hypoid import _742
from mastapy._internal.python_net import python_net_import

_HYPOID_GEAR_SET_CREATION_OPTIONS = python_net_import('SMT.MastaAPI.Gears.GearDesigns.CreationOptions', 'HypoidGearSetCreationOptions')


__docformat__ = 'restructuredtext en'
__all__ = ('HypoidGearSetCreationOptions',)


class HypoidGearSetCreationOptions(_871.GearSetCreationOptions['_742.HypoidGearSetDesign']):
    '''HypoidGearSetCreationOptions

    This is a mastapy class.
    '''

    TYPE = _HYPOID_GEAR_SET_CREATION_OPTIONS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'HypoidGearSetCreationOptions.TYPE'):
        super().__init__(instance_to_wrap)
