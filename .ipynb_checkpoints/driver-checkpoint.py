import sys
import papermill as pm

# Get the uploaded image path from command-line arguments
input_image_path = sys.argv[1]

# Run the Jupyter notebook with the input image path as a parameter
input_notebook = "preprocessing.ipynb"
output_notebook = "executed_project.ipynb"

pm.execute_notebook(
    input_path=input_notebook,
    output_path=output_notebook,
    parameters={"image_path": input_image_path}
)

print("Notebook executed successfully. Output image should be in output.png")
