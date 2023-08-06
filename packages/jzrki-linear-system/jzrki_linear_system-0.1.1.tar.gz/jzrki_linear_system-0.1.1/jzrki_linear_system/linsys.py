from decimal import Decimal, getcontext
from copy import deepcopy

from .vector import Vector
from .hyperplane import Hyperplane

getcontext().prec = 30


class LinearSystem(object):

    ALL_PLANES_MUST_BE_IN_SAME_DIM_MSG = 'All planes in the system should live in the same dimension'
    NO_SOLUTIONS_MSG = 'No solutions'
    INF_SOLUTIONS_MSG = 'Infinitely many solutions'

    def __init__(self, planes):
        try:
            d = planes[0].dimension
            for p in planes:
                assert p.dimension == d

            self.planes = planes
            self.dimension = d

        except AssertionError:
            raise Exception(self.ALL_PLANES_MUST_BE_IN_SAME_DIM_MSG)

    def __eq__(self, other):
        return self.planes == other.planes

    def swap_rows(self, row1, row2):
        self[row1], self[row2] = self[row2], self[row1]

    def multiply_coefficient_and_row(self, coefficient, row):
        self[row] *= coefficient

    def add_multiple_times_row_to_row(self, coefficient, row_to_add, row_to_be_added_to):
        self[row_to_be_added_to] += self[row_to_add] * coefficient

    def indices_of_first_nonzero_terms_in_each_row(self):
        num_equations = len(self)
        num_variables = self.dimension

        indices = [-1] * num_equations

        for i,p in enumerate(self.planes):
            try:
                indices[i] = p.first_nonzero_index(p.normal_vector.coordinates)
            except Exception as e:
                if str(e) == Hyperplane.NO_NONZERO_ELTS_FOUND_MSG:
                    continue
                else:
                    raise e

        return indices


    def __len__(self):
        return len(self.planes)


    def __getitem__(self, i):
        return self.planes[i]


    def __setitem__(self, i, x):
        try:
            assert x.dimension == self.dimension
            self.planes[i] = x

        except AssertionError:
            raise Exception(self.ALL_PLANES_MUST_BE_IN_SAME_DIM_MSG)


    def __str__(self):
        ret = 'Linear System:\n'
        temp = ['Equation {}: {}'.format(i+1,p) for i,p in enumerate(self.planes)]
        ret += '\n'.join(temp)
        return ret

    def compute_triangular_form(self):
        system = deepcopy(self)
        
        num_eq = len(system)
        num_var = system.dimension
        
        j = 0
        for i in range(num_eq):
            while j < num_var:
                leading_coefficient = MyDecimal(system[i].normal_vector[j])
                if leading_coefficient.is_near_zero():
                    swap_succeed = system.swap_topmost_below(i,j)
                    if not swap_succeed:
                        j += 1
                        continue
                system.clear_all_var_below(i,j)
                j+=1
                break
        return system
        
    def swap_topmost_below(self, row, col):
        for k in range(row+1, len(self)):
            leading_coefficient = MyDecimal(self[k].normal_vector[col])
            if not leading_coefficient.is_near_zero():
                self.swap_rows(row, k)
                return True
        return False
    
    def clear_all_var_below(self,row, col):
        for k in range(row+1, len(self)):
            coefficient = - self[k].normal_vector[col] / self[row].normal_vector[col]
            self.add_multiple_times_row_to_row(coefficient, row, k)
        
    def compute_rref(self):
        tf = self.compute_triangular_form()
        
        num_eq = len(tf)
        num_var = tf.dimension
        
        leading_indices = tf.indices_of_first_nonzero_terms_in_each_row()
        for i in range(num_eq)[::-1]:
            j = leading_indices[i]
            if j < 0:
                continue
            tf.norm_leading_coefficient(i, j)
            tf.clear_all_var_above(i, j)
        return tf

    def norm_leading_coefficient(self, row, col):
        self.multiply_coefficient_and_row(MyDecimal(1.0) / self[row].normal_vector[col], row)
        
    def clear_all_var_above(self, row, col):
        for k in range(row)[::-1]:
            coefficient = - self[k].normal_vector[col] / self[row].normal_vector[col]
            self.add_multiple_times_row_to_row(coefficient, row, k)
            
    def compute_solutions(self):
        try:
            return self.GE_extract_solutions()
        except Exception as e:
            if str(e) == self.NO_SOLUTIONS_MSG:
                return str(e)
            else:
                raise e

    def GE_extract_solutions(self):
        rref = self.compute_rref()
        
        rref.raise_exception_of_contradictory_eq()
        
        direction_vectors = rref.extract_dv()
        basepoint = rref.extract_bp()
        return Parametrization(basepoint, direction_vectors)
                
    def raise_exception_of_contradictory_eq(self):
        for p in self.planes:
            try:
                p.first_nonzero_index(p.normal_vector.coordinates)
                
            except Exception as e:
                if str(e) == p.NO_NONZERO_ELTS_FOUND_MSG:
                    constant_term = MyDecimal(p.constant_term)
                    if not constant_term.is_near_zero():
                        raise Exception(self.NO_SOLUTIONS_MSG)
                else:
                    raise e
                    
    def extract_dv(self):
        num_var = self.dimension
        pivot_indices = self.indices_of_first_nonzero_terms_in_each_row()
        free_var_indices = set(range(num_var)) - set(pivot_indices)
        
        dv = []
        
        for free_var in free_var_indices:
            v_coords = [0]*num_var
            v_coords[free_var] = 1
            for i,p in enumerate(self.planes):
                pv = pivot_indices[i]
                if pv < 0:
                    break
                v_coords[pv] = -p.normal_vector[free_var]
            dv.append(Vector(v_coords))
        return dv
    
    def extract_bp(self):
        num_var = self.dimension
        pivot_indices = self.indices_of_first_nonzero_terms_in_each_row()
        
        bp_coords = [0]*num_var
        
        for i,p in enumerate(self.planes):
            pv = pivot_indices[i]
            if pv < 0:
                break
            bp_coords[pv] = p.constant_term
        return Vector(bp_coords)

            
    def compute_solutions_my_way(self):
        rref = self.compute_rref()
        pivot_indices = rref.indices_of_first_nonzero_terms_in_each_row()
        num_pivots = sum([1 if ind >= 0 else 0 for ind in pivot_indices])
        num_var = rref.dimension

        
        for i in range(len(rref)):
            if (pivot_indices[i] < 0) and (not MyDecimal(rref[i].constant_term).is_near_zero()):
                return str(Exception(rref.NO_SOLUTIONS_MSG))
        if num_pivots == num_var:
            return Vector([rref[i].constant_term for i in range(num_var)])
        else:
            return str(Exception(rref.INF_SOLUTIONS_MSG))

class MyDecimal(Decimal):
    def is_near_zero(self, eps=1e-10):
        return abs(self) < eps
    
class Parametrization(object):
    
    BASEPT_AND_DIR_VECTORS_MUST_BE_IN_SAME_SIM_MSG = (
        'The basepoint and direction vectors should all live in the same dimension')
    
    def __init__(self, basepoint, direction_vectors):
        
        self.basepoint = basepoint
        self.direction_vectors = direction_vectors
        self.dimension = self.basepoint.dimension
        
        try:
            for v in direction_vectors:
                assert v.dimension == self.dimension
                
        except AssertionError:
                raise Exception(BASEPT_AND_DIR_VECTORS_MUST_BE_IN_SAME_SIM_MSG)
                
    def __str__(self):
        ret = ''
        for i in range(self.dimension):
            temp = 'x_{} = {}'.format(i,self.basepoint[i])
            for j in range(len(self.direction_vectors)):
                temp += '+ ' + str(self.direction_vectors[j].coordinates[i]) + ' t_{}'.format(j+1)
            ret += '\n' + temp
        return ret