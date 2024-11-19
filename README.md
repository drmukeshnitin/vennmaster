**Venn-Master-Venn Diagram ToolOverview**

The Venn-Master-Venn Diagram Tool is a Python-based standalone GUI application designed for creating Venn diagrams and generating detailed reports from multiple data sources. Users can input up to 4 datasets to visualize unique and overlapping values among them. For datasets beyond this limit, the tool generates a comprehensive report of unique and common values across all input files. 

The tool is user-friendly, offers a colorful interface, and includes a download feature for saving results.

![Screenshot from 2024-11-20 01-29-55](https://github.com/user-attachments/assets/83530342-3d70-4458-9694-62827362b247)



Venn-Master-Venn Diagram ToolKey Features

- Multi-Set Venn Diagram Visualization:
  - Supports Venn diagrams for up to 4 datasets.
  - Automatically generates and labels diagrams.
  - Saves diagrams as PNG files.

- Unique and Common Value Analysis:
  - Generates an Excel report (`unique_and_common_values_analysis_report.xlsx`) summarizing unique and overlapping values.
  - Handles datasets beyond 4 entries in the analysis.

- File Upload & Text Entry:
  - Upload files or directly input data via text boxes.
  - Assign custom labels for each dataset.

- Download Functionality:
  - Save Venn diagrams and analysis reports to a user-specified directory.

- Intuitive GUI:
  - Add multiple datasets dynamically.
  - Error handling for invalid or insufficient inputs.
  - Responsive design with progress notifications.



Venn-Master-Venn Diagram ToolRequirements

- Python Version: 3.8 or above
- Dependencies:
  - `tkinter` (Standard library for GUI in Python)
  - `matplotlib`
  - `matplotlib-venn`
  - `venn` (For handling 4-set Venn diagrams)
  - `pandas`

To install the dependencies, run:

```bash
pip install matplotlib matplotlib-venn venn pandas
```

Venn-Master-Venn Diagram ToolInstallation

1. Clone the repository or download the tool script:
   ```bash
   git clone https://github.com/your-repo/venn-master-tool.git
   cd venn-master-tool
   ```

2. Install the required dependencies (see above).

3. Run the tool:
   ```bash
   python venn_tool.py
   ```



Venn-Master-Venn Diagram ToolHow to Use

1. Add Data Entries:
   - Click "Add Data Entry" to add a new dataset.
   - Upload a file or paste text data into the provided text box.
   - Optionally, assign a custom label for the dataset.

2. Generate Venn Diagram and Report:
   - After adding at least 2 datasets, click "Generate Venn Diagram and Table."
   - The tool will create a Venn diagram (for up to 4 datasets) and an Excel report.

3. Download Results:
   - Click "Download Results" to save the Venn diagram and Excel report to a directory of your choice.



Venn-Master-Venn Diagram ToolOutput Files

- Venn Diagram: `venn_diagram.png` (up to 4 datasets)
- Analysis Report: `unique_and_common_values_analysis_report.xlsx`



Venn-Master-Venn Diagram ToolError Handling

- Insufficient Data: Displays an error if fewer than 2 datasets are provided.
- File Errors: Alerts users if a file cannot be found or uploaded.
- Dataset Limitations: Warns users when input exceeds 4 datasets (analysis still proceeds).



Venn-Master-Venn Diagram ToolCustomization

- Update the default colors and fonts by modifying the `VennDiagramTool` class.
- Change the default file extensions or add support for additional formats in the `browse_file` method.



Venn-Master-Venn Diagram ToolFuture Enhancements

- Support for more complex visualizations for datasets larger than 4.
- Additional customization options for Venn diagram aesthetics.
- Integration with cloud storage for sharing results.



Venn-Master-Venn Diagram ToolLicense

This project is licensed under the MIT License.



Venn-Master-Venn Diagram ToolContact

For any issues or suggestions, please reach out to:

- Author: Dr Mukesh nitin
- Email: drrmukeshnitin@gmail.com
- GitHub: https://github.com/drmukeshnitin/vennmaster
