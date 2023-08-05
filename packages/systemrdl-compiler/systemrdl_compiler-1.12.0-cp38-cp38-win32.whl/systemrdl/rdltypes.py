import enum
import inspect
from collections import OrderedDict

from .core import rdlformatcode
from . import component as comp

class AutoEnum(enum.Enum):
    def __new__(cls):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

#===============================================================================
class AccessType(AutoEnum):
    #: Not Accessible
    na = ()

    #: Readable and writable
    rw = ()

    #: Read-only
    r = ()

    #: Write-only
    w = ()

    #: Readable and writable. After a reset occurs, can only be written once.
    rw1 = ()

    #: Write-only. After a reset occurs, can only be written once.
    w1 = ()

class OnReadType(AutoEnum):
    #: Cleared on read
    rclr = ()

    #: Set on read
    rset = ()

    #: User-defined read side-effect
    ruser = ()

class OnWriteType(AutoEnum):
    #: Bitwise write one to set
    woset = ()

    #: Bitwise write one to clear
    woclr = ()

    #: Bitwise write one to toggle
    wot = ()

    #: Bitwise write zero to set
    wzs = ()

    #: Bitwise write zero to clear
    wzc = ()

    #: Bitwise write zero to toggle
    wzt = ()

    #: All bits are cleared on write
    wclr = ()

    #: All bits are set on write
    wset = ()

    #: Write modification is user-defined
    wuser = ()

class AddressingType(AutoEnum):
    #: Components are packed tightly together
    compact = ()

    #: Components are packed so each component’s start address is a multiple of its size
    regalign = ()

    #: Same as regalign, except arrays are aligned to their entire size
    fullalign = ()

class PrecedenceType(AutoEnum):
    #: Hardware writes take precedence over software
    hw = ()

    #: Software writes take precedence over hardware
    sw = ()

class InterruptType(AutoEnum):
    """
    A field's interrupt type is set when using an RDL interrupt property modifier:

    .. code-block:: systemrdl

        field f {
            negedge intr;
        };

    The modifier is stored in the internal "intr type" property. (note the intentional space in the name)

    It can be fetched the same way as other properties:

    .. code-block:: python

        intr_type = my_field_node.get_property("intr type")

    """
    #: Interrupt when asserted and maintained
    level = ()

    #: Interrupt on low-to-high transition
    posedge = ()

    #: Interrupt on high-to-low transition
    negedge = ()

    #: Interrupt on any transition
    bothedge = ()

#===============================================================================
class UserEnum(enum.Enum):
    """
    All user-defined enumerations are based on this class.

    UserEnum types can be identified using: :meth:`is_user_enum`
    """
    def __init__(self, value, rdl_name, rdl_desc):
        self._value_ = value
        self._rdl_name_ = rdl_name
        self._rdl_desc_ = rdl_desc

    @property
    def rdl_desc(self):
        """
        Enum entry's ``desc`` property
        """
        return self._rdl_desc_

    @property
    def rdl_name(self):
        """
        Enum entry's ``name`` property
        """
        return self._rdl_name_

    def get_html_desc(self, markdown_inst=None):
        """
        Translates the enum's 'desc' property into HTML.

        Any RDLFormatCode tags used are converted to HTML.
        The text is also fed through a Markdown processor.

        The additional Markdown processing allows designers the choice to use a
        more modern lightweight markup language as an alternative to SystemRDL's
        "RDLFormatCode".

        Parameters
        ----------
        markdown_inst: ``markdown.Markdown``
            Override the class instance of the Markdown processor.
            See the `Markdown module <https://python-markdown.github.io/reference/#Markdown>`_
            for more details.

        Returns
        -------
        str or None
            HTML formatted string.
            If enum entry does not have a description, returns ``None``


        .. versionchanged:: 1.6
            Added ``markdown_inst`` option.
        """
        desc_str = self._rdl_desc_
        if desc_str is None:
            return None
        return rdlformatcode.rdlfc_to_html(desc_str, md=markdown_inst)

    def get_html_name(self):
        """
        Translates the enum's 'name' property into HTML.

        Any RDLFormatCode tags used are converted to HTML.

        Returns
        -------
        str or None
            HTML formatted string.
            If enum entry does not have an explicitly set name, returns ``None``


        .. versionadded:: 1.8
        """
        name_str = self._rdl_name_
        if name_str is None:
            return None
        return rdlformatcode.rdlfc_to_html(name_str, is_desc=False)

    @classmethod
    def _set_parent_scope(cls, scope):
        cls._parent_scope = scope

    @classmethod
    def get_parent_scope(cls):
        """
        Returns reference to parent component that contains this type definition.
        """
        return getattr(cls, "_parent_scope", None)

    @classmethod
    def get_scope_path(cls, scope_separator="::"):
        """
        Generate a string that represents this enum's declaration namespace
        scope.

        Parameters
        ----------
        scope_separator: str
            Override the separator between namespace scopes
        """
        parent_scope = cls.get_parent_scope()
        if parent_scope is None:
            # Importer likely never set the scope
            return ""
        elif isinstance(parent_scope, comp.Root):
            # Declaration was in root scope
            return ""
        else:
            # Get parent definition's scope path
            parent_path = parent_scope.get_scope_path(scope_separator)

            # Extend it with its scope name
            if parent_path:
                return(
                    parent_path
                    + scope_separator
                    + parent_scope._scope_name
                )
            else:
                return parent_scope._scope_name


    def __int__(self):
        return self.value

    def __bool__(self):
        return bool(self.value)

    def __deepcopy__(self, memo):
        # Do not deepcopy enumerations
        return self


def is_user_enum(t):
    """
    Test if type ``t`` is a :class:`~UserEnum`

    .. note:: Returns false if ``t`` is referencing a UserEnum value member
    """
    return inspect.isclass(t) and issubclass(t, UserEnum)

#===============================================================================
class UserStruct:
    """
    All user-defined structs are based on this class.

    UserStruct types can be identified using: :meth:`is_user_struct`

    Values of struct members are accessed as read-only object attributes.

    For example, the following RDL struct literal:

    .. code-block:: systemrdl

        struct my_struct {
            longint foo;
            longint bar;
        };
        ...
        my_struct_prop = my_struct'{foo:42, bar:123};

    ... can be queried in Python as follows:

    .. code-block:: python

        prop = node.get_property("my_struct_prop")

        foo = prop.foo
        bar = getattr(prop, "bar")

    If necessary, a list of a UserStruct's member names can be accessed by:

    .. code-block:: python

        member_names = prop._members.keys()
    """

    _members = OrderedDict()
    _is_abstract = True

    def __init__(self, values):
        """
        Create an instance of the struct

        values is a dictionary of {member_name : value}
        """
        if self._is_abstract:
            raise TypeError("Cannot create instance of an abstract struct type")

        # Make sure values dict matches the members allowed
        if set(values.keys()) != set(self._members.keys()):
            raise ValueError("Cannot map 'values' to this struct")

        self._values = values

    @classmethod
    def define_new(cls, name, members, is_abstract=False):
        """
        Define a new struct type derived from the current type.

        Parameters
        ----------
        name: str
            Name of the struct type
        members: {member_name : type}
            Dictionary of struct member types.
        is_abstract: bool
            If set, marks the struct as abstract.
        """
        m = OrderedDict(cls._members)

        # Make sure derivation does not have any overlapping keys with its parent
        if set(m.keys()) & set(members.keys()):
            raise ValueError("'members' contains keys that overlap with parent")

        m.update(members)

        dct = {
            '_members' : m,
            '_is_abstract': is_abstract,
        }
        newcls = type(name, (cls,), dct)
        return newcls

    def __getattr__(self, name):
        if name == "__setstate__":
            raise AttributeError(name)
        if name in self._values:
            return self._values[name]
        else:
            raise AttributeError("'%s' object has no attribute '%s'" % (type(self).__name__, name))

    @classmethod
    def _set_parent_scope(cls, scope):
        cls._parent_scope = scope

    @classmethod
    def get_parent_scope(cls):
        """
        Returns reference to parent component that contains this type definition.
        """
        return getattr(cls, "_parent_scope", None)

    @classmethod
    def get_scope_path(cls, scope_separator="::"):
        """
        Generate a string that represents this enum's declaration namespace
        scope.

        Parameters
        ----------
        scope_separator: str
            Override the separator between namespace scopes
        """
        parent_scope = cls.get_parent_scope()
        if parent_scope is None:
            # Importer likely never set the scope
            return ""
        elif isinstance(parent_scope, comp.Root):
            # Declaration was in root scope
            return ""
        else:
            # Get parent definition's scope path
            parent_path = parent_scope.get_scope_path(scope_separator)

            # Extend it with its scope name
            if parent_path:
                return(
                    parent_path
                    + scope_separator
                    + parent_scope._scope_name
                )
            else:
                return parent_scope._scope_name

    def __repr__(self):
        return "<struct '%s' %s at 0x%x>" % (
            self.__class__.__qualname__,
            "(%s)" % ", ".join(self._members.keys()),
            id(self)
        )

def is_user_struct(t):
    """
    Test if type ``t`` is a :class:`~UserStruct`
    """
    return inspect.isclass(t) and issubclass(t, UserStruct)

#===============================================================================
class ComponentRef:
    """
    Container for hierarchical component instance references.
    This is used internally to store information about the reference
    When a user requests the reference value, it is resolved into a Node object
    """

    def __init__(self, ref_root, ref_elements):
        # Handle to the component definition where ref_elements is relative to
        # This is the original_def, and NOT the actual instance
        self.ref_root = ref_root

        # List of hierarchical reference element tuples that make up the path
        # to the reference.
        # Path is relative to the instance of ref_root
        # Each tuple in the list represents a segment of the path:
        # [
        #   ( <ID string> , [ <Index int> , ... ], SourceRef ),
        #   ( <ID string> , None, SourceRef )
        # ]
        self.ref_elements = ref_elements

    def build_node_ref(self, assignee_node, env):
        from .node import AddressableNode # pylint: disable=import-outside-toplevel

        current_node = assignee_node
        # Traverse up from assignee until ref_root is reached
        while True:
            if current_node is None:
                raise RuntimeError("Upwards traverse to ref_root failed")
            if current_node.inst.original_def is self.ref_root:
                break
            current_node = current_node.parent

        for inst_name, idx_list, name_src_ref in self.ref_elements:
            # find instance
            current_node = current_node.get_child_by_name(inst_name)
            if current_node is None:
                raise RuntimeError

            # Check if indexes are valid
            for i, idx in enumerate(idx_list):
                if idx >= current_node.inst.array_dimensions[i]:
                    env.msg.fatal(
                        "Array index out of range. Expected 0-%d, got %d."
                        % (current_node.inst.array_dimensions[i]-1, idx),
                        name_src_ref
                    )

            # Assign indexes if appropriate
            if (isinstance(current_node, AddressableNode)) and current_node.inst.is_array:
                current_node.current_idx = idx_list

        return current_node

#===============================================================================
class PropertyReference:
    """
    Base class for all property references used in RHS of an expression.

    The PropertyReference object represents the expression's reference target.
    Details of the reference can be determined using its ``node`` and ``name``
    variables.

    For example, the following property assignment:

    .. code-block:: systemrdl

        reg {
            ...
            fieldX->next = fieldY->intr;
        } my_reg;

    ... can be queried as follows:

    .. code-block:: python

        fieldX = my_reg.get_child_by_name("fieldX")
        fieldY = my_reg.get_child_by_name("fieldY")

        next_prop = fieldX.get_property("next")
        print(next_prop.node == fieldY) # prints: True
        print(next_prop.name) # prints: "intr"

    """
    allowed_inst_type = None

    def __init__(self, src_ref, env, comp_ref):
        self.env = env
        self.src_ref = src_ref
        self._comp_ref = comp_ref

        #: Node object that represents the component instance from which the
        #: property is being referenced.
        self.node = None

    @property
    def name(self):
        """
        Name of the property being referenced
        """
        return self.get_name()

    @classmethod
    def get_name(cls):
        return cls.__name__.replace("PropRef_", "")

    def _resolve_node(self, assignee_node):
        self.node = self._comp_ref.build_node_ref(assignee_node, self.env)

    def _validate(self):
        pass

#===============================================================================
class ArrayPlaceholder():
    """
    Placeholder class to describe array types

    Once elaborated, arrays are converted to Python lists
    In the meantime, this placeholder is used to communicate expected type
    information during compilation type checking
    """
    def __init__(self, element_type):
        self.element_type = element_type

    def __eq__(self, other):
        if isinstance(other, ArrayPlaceholder):
            return self.element_type == other.element_type
        else:
            return False

#===============================================================================
def get_rdltype(value):
    """
    Given a value, return the type identifier object used within the RDL compiler
    If not a supported type, return None
    """

    if isinstance(value, (int, bool, str)):
        # Pass canonical types as-is
        return type(value)
    elif is_user_enum(type(value)):
        return type(value)
    elif is_user_struct(type(value)):
        return type(value)
    elif isinstance(value, enum.Enum):
        return type(value)
    elif isinstance(value, list):
        # Create ArrayPlaceholder representation
        # Determine element type and make sure it is uniform
        array_el_type = None
        for el in value:
            el_type = get_rdltype(el)
            if el_type is None:
                return None

            if (array_el_type is not None) and (el_type != array_el_type):
                return None
            array_el_type = el_type
        return ArrayPlaceholder(array_el_type)
    else:
        return None
