import papermill as pm
import sys

# Get the image path from command line arguments
image_path = sys.argv[1]

# Define input and output notebook paths
input_notebook = 'project.ipynb'
output_notebook = 'output.ipynb'

# Execute the notebook with the image_path parameter
pm.execute_notebook(
    input_path=input_notebook,
    output_path=output_notebook,
    parameters={'image_path': image_path}
)