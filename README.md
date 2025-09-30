# Azure-Devops-Scripts

A collection of Azure DevOps utilities and automation scripts.

## Azure GitHub Organization Checker

This project is designed to interact with GitHub and Azure DevOps APIs to check all repositories in a specified GitHub organization. It gathers repository details, including size, and manages team and user lists in Azure DevOps.

### Project Structure

```
azure-github-org-checker
├── src
│   ├── main.py               # Entry point of the application
│   ├── github_api.py         # Functions to interact with the GitHub API
│   ├── azure_devops_api.py   # Functions to interact with the Azure DevOps API
│   ├── utils.py              # Utility functions for data processing
│   └── types
│       └── index.py          # Data types and structures used in the project
├── requirements.txt          # Project dependencies
├── .gitignore                # Files and directories to ignore by Git
├── README.md                 # Documentation for the project
└── azure-pipelines.yml       # Azure DevOps pipeline configuration
```

### Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone https://github.com/Prathyushanuthi-hub/Azure-Devops-Scripts.git
   cd Azure-Devops-Scripts/azure-github-org-checker
   ```

2. **Install Dependencies**
   It is recommended to use a virtual environment. You can create one using `venv`:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
   Then install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configuration**
   Ensure you have the necessary API tokens for GitHub and Azure DevOps. You may need to set these as environment variables or configure them in a separate configuration file.

### Usage

To run the application, execute the following command:
```bash
python src/main.py
```

### Functionality

- **Check Repositories**: The application lists all repositories in the specified GitHub organization and retrieves their details, including size.
- **Manage Teams and Users**: It adds repositories to specified teams and user lists in Azure DevOps.

## Contributing

Feel free to submit issues or pull requests to enhance the functionality of this project.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
