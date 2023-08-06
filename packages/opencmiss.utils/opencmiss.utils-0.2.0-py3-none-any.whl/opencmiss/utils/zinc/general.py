"""
General utilities for working with the OpenCMISS-Zinc library.
"""
from opencmiss.zinc.context import Context


class AbstractNodeDataObject(object):

    def __init__(self, field_names, time_sequence=None, time_sequence_field_names=None):
        self._field_names = field_names
        self._time_sequence = time_sequence if time_sequence else []
        self._time_sequence_field_names = time_sequence_field_names if time_sequence_field_names else []
        self._check_field_names()

    def _check_field_names(self):
        for field_name in self._field_names:
            if not hasattr(self, field_name):
                raise NotImplementedError('Missing data method for field: %s' % field_name)

    def get_field_names(self):
        return self._field_names

    def set_field_names(self, field_names):
        self._field_names = field_names
        self._check_field_names()

    def get_time_sequence(self):
        return self._time_sequence

    def set_time_sequence(self, time_sequence):
        self._time_sequence = time_sequence

    def get_time_sequence_field_names(self):
        return self._time_sequence_field_names

    def set_time_sequence_field_names(self, time_sequence_field_names):
        self._time_sequence_field_names = time_sequence_field_names


class ChangeManager:
    """
    Python Context Manager minimising change messages for a Zinc object,
    for use whenever making multiple changes to the object or objects it owns.
    Ensures beginChange, endChange are always called, even with exceptions.
    Usage:
    with ChangeManager(object):
        # make multiple changes to object or objects it owns
    """

    def __init__(self, change_object):
        """
        :param change_object: Zinc object with beginChange/endChange methods.
        """
        self._object = change_object

    def __enter__(self):
        self._object.beginChange()
        return self

    def __exit__(self, *args):
        self._object.endChange()


def define_standard_graphics_objects(context: Context):
    """
    Defines Zinc standard objects for use in graphics, including
    a number of graphical materials and glyphs.
    """
    glyphmodule = context.getGlyphmodule()
    glyphmodule.defineStandardGlyphs()
    materialmodule = context.getMaterialmodule()
    materialmodule.defineStandardMaterials()


def create_node(field_module, data_object, identifier=-1, node_set_name='nodes', time=None):
    """
    Create a Node in the field_module using the data_object.  The data object must supply a 'get_field_names' method
    and a 'get_time_sequence' method.  Derive a node data object from the 'AbstractNodeDataObject' class to ensure
    that the data object class meets it's requirements.

    Optionally use the identifier to set the identifier of the Node created, the time parameter to set
    the time value in the cache, or the node_set_name to specify which node set to use the default node set
    is 'nodes'.

    :param field_module: The field module that has at least the fields defined with names in field_names.
    :param data_object: The object that can supply the values for the field_names through the same named method.
    :param identifier: Identifier to assign to the node. Default value is '-1'.
    :param node_set_name: Name of the node set to create the node in.
    :param time: The time to set for the node, defaults to None for nodes that are not time aware.
    :return: The node identifier assigned to the created node.
    """
    # Find a special node set named 'nodes'
    node_set = field_module.findNodesetByName(node_set_name)
    node_template = node_set.createNodetemplate()

    # Set the finite element coordinate field for the nodes to use
    fields = []
    field_names = data_object.get_field_names()
    for field_name in field_names:
        fields.append(field_module.findFieldByName(field_name))
        node_template.defineField(fields[-1])
    if data_object.get_time_sequence():
        time_sequence = field_module.getMatchingTimesequence(data_object.get_time_sequence())
        for field_name in data_object.get_time_sequence_field_names():
            time_sequence_field = field_module.findFieldByName(field_name)
            node_template.setTimesequence(time_sequence_field, time_sequence)
    field_cache = field_module.createFieldcache()
    node = node_set.createNode(identifier, node_template)
    # Set the node coordinates, first set the field cache to use the current node
    field_cache.setNode(node)
    if time:
        field_cache.setTime(time)
    # Pass in floats as an array
    for i, field in enumerate(fields):
        field_name = field_names[i]
        field_value = getattr(data_object, field_name)()
        if isinstance(field_value, ("".__class__, u"".__class__)):
            field.assignString(field_cache, field_value)
        else:
            field.assignReal(field_cache, field_value)

    return node.getIdentifier()


defineStandardGraphicsObjects = define_standard_graphics_objects
createNode = create_node
