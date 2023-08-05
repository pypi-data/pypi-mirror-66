# pymization
Simple solver for optimization problems.

CDS implemented
## Installation

```bash
pip install pymization
```

## Example

Code to use CDS given a matrix where rows are jobs and columns are machines.

```python
import pymization as pym


solver = pym.Solver("CDS")
solver.load_data_from_matrix(matrix)
solver.run()
```

If you want to use some functions developed on CDS you can use as the follow

```python
import pymization as pym

solver = pym.Solver("CDS")
solver.load_data_from_matrix(matrix)
solver.load_model()
solver.model.get_sets() # Retrieves order sets to Johnson's algorithm
solver.model.min_makespan(job_sequence) # Given a Johnson's ordered jobs calculate min_makespan and actualize objective_function

solver.model.final_sequence
solver.model.objective_function
```

### Work in progress

Any inquirements:

- Nicolas Camus: ncamusf@gmail.com
- Maurice Poirrier: maurice@merkenlabs.com
