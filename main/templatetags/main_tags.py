from jinja2 import nodes
from jinja2.ext import Extension

class SetVariableExtension(Extension):
    tags = {'set'}

    def parse(self, parser):
        # Get the tag token and the variable name
        lineno = next(parser.stream).lineno
        variable_name = parser.parse_assign_target()

        # Consume the equal sign and parse the expression
        parser.stream.expect('assign')
        expression = parser.parse_expression()

        # Create a node for the assignment
        assignment_node = nodes.Assign(
            target=variable_name,
            node=expression,
            lineno=lineno
        )

        # Return the assignment node
        return assignment_node