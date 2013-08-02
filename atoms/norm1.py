from atom import Atom
import cvxpy.expressions.types as types
from cvxpy.expressions.variable import Variable
from cvxpy.expressions.curvature import Curvature
from cvxpy.expressions.shape import Shape
from cvxpy.constraints.affine import AffEqConstraint, AffLeqConstraint
from monotonicity import Monotonicity

class norm1(Atom):
    """ L1 norm sum(|x|) """
    def __init__(self, x):
        self._shape = Shape(1,1)
        super(norm1, self).__init__(x)

    # Default curvature.
    def base_curvature(self):
        return Curvature.CONVEX

    def monotonicity(self):
        return [Monotonicity.NONMONOTONIC]

    # Verify that the argument x is a vector.
    def validate_arguments(self):
        rows,cols = self.args[0].size
        if cols != 1:
            raise Exception("The argument '%s' to norm1 must resolve to a vector." 
                % self.args[0].name())

    @staticmethod
    def graph_implementation(var_args):
        x = var_args[0]
        rows,cols = x.size
        t = Variable(rows)
        ones = types.constant()(rows*[[1]])
        return (ones*t, [AffLeqConstraint(-t, x), AffLeqConstraint(x,t)])