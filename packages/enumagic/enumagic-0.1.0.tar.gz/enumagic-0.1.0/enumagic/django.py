"""Special enums for Django."""

# Copyright (c) 2020 ObserverOfTime
#
# This software is provided 'as-is', without any express or implied
# warranty. In no event will the authors be held liable for any damages
# arising from the use of this software.
#
# Permission is granted to anyone to use this software for any purpose,
# including commercial applications, and to alter it and redistribute it
# freely, subject to the following restrictions:
#
# 1. The origin of this software must not be misrepresented; you must not
#   claim that you wrote the original software. If you use this software
#   in a product, an acknowledgment in the product documentation would be
#   appreciated but is not required.
# 2. Altered source versions must be plainly marked as such, and must not be
#   misrepresented as being the original software.
# 3. This notice may not be removed or altered from any source distribution.

from enum import Enum, EnumMeta
from typing import Any, Iterator, Type, TypeVar, Tuple

_VT = TypeVar('_VT')
_ET = TypeVar('_ET', bound=Type[Enum])


class ChoiceMeta(EnumMeta):
    """Choice enum metaclass."""
    def __new__(meta, *args, **kwargs):
        cls = super().__new__(meta, *args, **kwargs)
        cls.do_not_call_in_templates = True
        return cls

    def __iter__(cls) -> Iterator[Tuple[str, _VT]]:
        """
        Iterate over the entries of the enum.

        Yields:
            :obj:`tuple` of :obj:`str`, :obj:`object` :

            The next tuple where the first element is the
            ``name`` of the enum instance and the second
            element is the ``value`` of the enum instance.

        Examples:
            >>> it = iter(ColorChoice)
            >>> next(it)
            ('RED', '#F00')
        """
        return ((e.name, e.value) for e in super().__iter__())

    def __contains__(cls, item: Any) -> bool:
        """
        Check whether the enum contains a certain item

        Args:
            item (:obj:`~typing.Any`): A string or enum instance.

        Returns:
            :obj:`bool`:

            ``True`` if the enum has a member that
            matches the given item, ``False`` otherwise.

        Raises:
            :obj:`TypeError`: If the item is not a string or enum instance.

        Examples:
            >>> 'GREEN' in ColorChoice
            True
            >>> 'CYAN' in ColorChoice
            False
        """
        if isinstance(item, str):
            return item in cls.__members__
        return super().__contains__(item)

    def __getitem__(cls, name: str) -> str:
        """
        Get the value of an enum member.

        Args:
            name (:obj:`str`): The name of the item.

        Returns:
            :obj:`str`: The value of the instance.

        Examples:
            >>> ColorChoice['GREEN']
            '#0F0'
        """
        return super().__getitem__(name).value


class ChoiceEnum(str, Enum, metaclass=ChoiceMeta):
    """
    Enum class that can be used as Django `field choices`_.

    Examples:
        >>> from django.db.models import CharField, Model
        >>> class ColorChoice(ChoiceEnum):
        ...     RED = '#F00'
        ...     GREEN = '#0F0'
        ...     BLUE = '#00F'
        >>> class Color(Model):
        ...     color = CharField(choices=ColorChoice)
        >>> example = Color(color=ColorChoice.RED)
        >>> example.get_color_display()
        '#F00'

    .. autoattribute:: do_not_call_in_templates
        :annotation: = True

        Prevent the Django `template system`_ from calling the enum.

    .. autoattribute:: __class__
        :annotation:

        alias of :class:`enumagic.django.ChoiceMeta`

    .. automethod:: __str__() -> str

    .. automethod:: __eq__(other: Any) -> bool

    .. _field choices:
        https://docs.djangoproject.com/en/3.0/ref
        /models/fields/#django.db.models.Field.choices

    .. _template system:
        https://docs.djangoproject.com/en/3.0/ref
        /templates/api/#variables-and-lookups
    """
    def __str__(self) -> str:
        """
        Return the instance as a string.

        Returns:
            :obj:`str`: The name of the instance.

        Examples:
            >>> str(ColorChoice.BLUE)
            'BLUE'
        """
        return self.name

    def __hash__(self) -> int:
        """
        Return the hash of the instance.

        Returns:
            :obj:`int`: The hashed name.

        Examples:
            >>> hash(ColorChoice.RED)
            364091286298964602
        """
        return hash(self.name)

    def __eq__(self, other: Any) -> bool:
        """
        Check whether the objects are equal.

        Args:
            other (:obj:`~typing.Any`): Another object.

        Returns:
            :obj:`bool`:

            ``True`` if the objects are equal as strings, ``False`` otherwise.

        Examples:
            >>> ColorChoice.GREEN == 'GREEN'
            True
        """
        return str(self) == str(other)
