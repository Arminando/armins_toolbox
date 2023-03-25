from collections import OrderedDict

import bpy
from bpy.props import BoolProperty
from ..log import logger

from ..utils.bl_class_registry import BlClassRegistry
from ..utils.property_class_registry import PropertyClassRegistry


@PropertyClassRegistry()
class _Properties:
    idname = "template"

    @classmethod
    def init_props(cls, scene):
        # Python defined properties here. Can be deleted if not needed.
        class Props():
            test_prop = None

        scene.at_props.template = Props()

        # Global property
        scene.at_test_prop = BoolProperty(
            name="Nice Prop Name",
            description="Prop Description",
            default=False
        )


    @classmethod
    def del_props(cls, scene):
        # Add props here for cleanup
        del scene.at_test_prop


@BlClassRegistry()
class AT_OT_Operator_Template(bpy.types.Operator):
    """
        Operator that does something.
    """

    bl_idname = "object.template_operator"
    bl_label = "Operator Name"
    bl_description = "Operator description"
    bl_options = {'REGISTER', 'UNDO'}

    # Operator properties (these will show up after the operator is executed)
    op_prop = BoolProperty(
        name="Test Prop",
        description="Test Prop description",
        default=False
    )

    @classmethod
    def poll(cls, context):
        # Write proper context check here
        return True

    def execute(self, context):
        # Instantiate props
        props = context.scene.at_props.template

        # Write the operator functionality here
        self.report({'INFO'}, "Operator executed successfully.")
        # Write to that custom prop if needed to pass info to other operators.
        props.test_prop = None
        logger.debug("Operator executed successfully.")

        return {'FINISHED'}