import re

REGEX_ROLE_NAME = r"^[a-zA-Z0-9\-\_\:]+$"
REGEX_ROLE_VALUE = r"^([a-zA-Z0-9\-\_,\.]*|\*)$"


def split_role(role):
    """
    :param role: Role string with format "name[value,value]"
    :type role: str
    :returns: tuple with role name and a set of values.
    :rtype: tuple[str, set[str]]

    Split a single role string.
    """
    regex = r"^([a-zA-Z0-9\-\_\:]+)(?:\[([a-zA-Z0-9\-\_,\.]*|\*)\])?$"
    matches = re.fullmatch(regex, role)
    if matches:
        name = matches.group(1)
        values = matches.group(2)
        return name, set(values.split(',')) if values else set()
    else:
        raise ValueError('Invalid role: `%s`' % role)


def join_role(name, values):
    """
    :param name: A valid role name.
    :type name: str
    :param values: A set of valid role values. (May be empty set)
    :type values: set[str]

    Returns a role string in the format: ``"name[value1,value2]"``.
    """
    if re.fullmatch(REGEX_ROLE_NAME, name) is None:
        raise ValueError('Invalid role name: `%s`' % name)
    for value in values:
        if re.fullmatch(REGEX_ROLE_VALUE, value) is None:
            raise ValueError('Invalid role value: `%s`' % value)
    if '*' in values and len(values) > 1:
        raise ValueError('Invalid role values: `%s`' % values)

    values_str = '[' + ','.join(sorted(values)) + ']' if values else ''
    return name + values_str


class Roles:
    """
    A class for managing access roles
    """

    def __init__(self, roles_str=None):
        """
        :param roles_str: A roles string with one ore more roles. E.g. "connect admin order[*]"
        :returns: Roles object
        :type roles_str: str
        :rtype: Roles
        Roles constructor
        """
        self._roles = dict()
        if roles_str:
            self.set_roles_str(roles_str)

    def __str__(self):
        return self.get_roles_str()

    def __repr__(self):
        return '<Roles:"%s">' % self.get_roles_str()

    def __contains__(self, item):
        return self.has_role(item)

    def __bool__(self):
        return len(self._roles) > 0

    def set_roles_str(self, roles_str):
        """
        :param roles_str: A roles string with one ore more roles.
        :type roles_str: object
        initialize Roles object with roles string
        """
        for role in roles_str.split():
            if role != '':
                name, values = split_role(role)
                self._roles[name] = values

    def get_roles_str(self):
        """
        :returns: A roles string.
        :rtype: str
        """
        return ' '.join([join_role(n, v) for n, v in sorted(self._roles.items())])

    def has_role(self, name):
        """
        :param name: Role name
        :type name: str
        :rtype: bool
        :returns: `True` if the Roles object contains role `name`.

        Checks if roles object contains given role.
        """
        return name in self._roles

    def get_roles(self):
        return self._roles.keys()

    def add_role(self, role_str):
        name, values = split_role(role_str)
        self._roles[name] = values

    def del_role(self, role):
        del self._roles[role]

    def get_role_values(self, role):
        if role not in self._roles:
            raise KeyError('Role does not exist: %s' % role)
        return self._roles[role]

    def has_role_value(self, role, value):
        if role not in self._roles:
            raise KeyError('Role does not exist: %s' % role)
        return role in self._roles and value in self._roles[role]

    def add_role_value(self, role, value):
        if role not in self._roles:
            raise KeyError('Role does not exist: %s' % role)
        if value == '*':
            self._roles[role] = ({'*'})
        elif re.fullmatch(REGEX_ROLE_VALUE, value):
            if '*' in self._roles[role]:
                raise ValueError('Cannot add role value: `%s` to `*`' % value)
            self._roles[role].add(value)
        else:
            raise ValueError('Invalid role value: `%s`' % value)

    def del_role_value(self, role, value):
        if role not in self._roles:
            raise KeyError('Role does not exist: %s' % role)
        if value == '*':
            self._roles[role] = set()
        else:
            self._roles[role].discard(value)

    def validate_roles(self, guard_roles, match_all=True):
        """
        :param guard_roles: Roles that must be satisfied.
        :type guard_roles: Roles
        :param match_all: Determines if all roles must be satisfied or only one role.
        :type match_all: bool
        :rtype: bool

        Checks if roles in `self` match the guard roles.
        """
        if not guard_roles:
            return True

        for (key, values) in guard_roles._roles.items():
            if key in self._roles:
                valid = True
                if values:
                    if '*' in self._roles[key]:
                        valid = True
                    elif match_all:
                        valid = self._roles[key].issuperset(values)
                    else:
                        valid = bool(values & self._roles[key])
            else:
                valid = False
            if valid and not match_all:
                return True
            if not valid and match_all:
                return False
        return valid

    def merge_roles(self, roles):
        """
        :param roles: Roles object to merge.
        :type roles: Roles
        :rtype: None

        Merge `self` with Roles object `roles`.
        """
        if not isinstance(roles, Roles):
            raise TypeError('Roles type expected')
        for key, values in roles._roles.items():
            if key in self._roles:
                self._roles[key] |= values
                if '*' in self._roles[key]:
                    self._roles[key] = {'*'}
            else:
                self._roles[key] = values

    def remove_roles(self, roles):
        """
        :param roles: Roles object with roles to remove.
        :type roles: Roles
        :rtype: None

        Removes keys and values from `self`.
        """
        if not isinstance(roles, Roles):
            raise TypeError('Roles type expected')
        for key, values in roles._roles.items():
            if key in self._roles:
                if len(values):
                    if '*' in values:
                        self._roles[key] = set()
                    else:
                        self._roles[key] -= values
                else:
                    del self._roles[key]
