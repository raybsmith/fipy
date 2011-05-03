import os
import sys

from solver import SolverConvergenceWarning, \
     PreconditionerWarning, \
     ScalarQuantityOutOfRangeWarning, \
     StagnatedSolverWarning, \
     MatrixIllConditionedWarning, \
     PreconditionerNotPositiveDefiniteWarning, \
     IllConditionedPreconditionerWarning, \
     MaximumIterationWarning

args = [s.lower() for s in sys.argv[1:]]

# any command-line specified solver takes precedence over environment variables

if '--no-pysparse' in args:
    solver = "no-pysparse"
elif '--trilinos' in args:
    solver = "trilinos"
elif '--pysparse' in args:
    solver = "pysparse"
elif '--pyamg' in args:
    solver = 'pyamg'             
elif '--scipy' in args:
    solver = 'scipy'
elif os.environ.has_key('FIPY_SOLVERS'):
    solver = os.environ['FIPY_SOLVERS'].lower()
else:
    solver = None

if solver == "pysparse":
    from fipy.solvers.pysparse import *
    from fipy.matrices.pysparseMatrix import _PysparseMeshMatrix
    _MeshMatrix =  _PysparseMeshMatrix

elif solver == "trilinos":
    from fipy.solvers.trilinos import *

    try:
        from fipy.matrices.pysparseMatrix import _PysparseMeshMatrix
        _MeshMatrix =  _PysparseMeshMatrix
    except ImportError:
        from fipy.matrices.trilinosMatrix import _TrilinosMeshMatrix
        _MeshMatrix =  _TrilinosMeshMatrix

elif solver == "scipy":
    from fipy.solvers.scipy import *
    from fipy.matrices.scipyMatrix import _ScipyMeshMatrix
    _MeshMatrix = _ScipyMeshMatrix
    
elif solver == "pyamg":
    from fipy.solvers.pyAMG import *
    from fipy.matrices.scipyMatrix import _ScipyMeshMatrix
    _MeshMatrix = _ScipyMeshMatrix
    
elif solver == "no-pysparse":
    from fipy.solvers.trilinos import *
    from fipy.matrices.trilinosMatrix import _TrilinosMeshMatrix
    _MeshMatrix =  _TrilinosMeshMatrix 

elif solver is None:
    # If no argument or environment variable, try importing them and seeing
    # what works
   
    try:
        from fipy.solvers.pysparse import *
        solver = "pysparse"
        from fipy.matrices.pysparseMatrix import _PysparseMeshMatrix
        _MeshMatrix =  _PysparseMeshMatrix
    except:
        try:
            from fipy.solvers.trilinos import *
            solver = "trilinos"
            try:
                from fipy.matrices.pysparseMatrix import _PysparseMeshMatrix
                _MeshMatrix =  _PysparseMeshMatrix
            except ImportError:
                from fipy.matrices.trilinosMatrix import _TrilinosMeshMatrix
                _MeshMatrix =  _TrilinosMeshMatrix
        except:
            try:
                from fipy.solvers.pyAMG import *
                solver = "pyamg"
                from fipy.matrices.scipyMatrix import _ScipyMeshMatrix
                _MeshMatrix = _ScipyMeshMatrix
            except:
                try:
                    from fipy.solvers.scipy import *
                    solver = "scipy"
                    from fipy.matrices.scipyMatrix import _ScipyMeshMatrix
                    _MeshMatrix = _ScipyMeshMatrix
                except:
                    raise ImportError, "Could not import any solver package. If you are using Trilinos, make sure you have all of the necessary Trilinos packages installed - Epetra, EpetraExt, AztecOO, Amesos, ML, and IFPACK." 
else:
    raise ImportError, 'Unknown solver package %s' % solver

    
