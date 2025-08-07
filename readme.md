# DevOps Midterm Project

This project is a full-stack bank loan management system built with **Flask**, Dockerized, and deployed on AWS Elastic Beanstalk using ECR. It simulates managing clients, creating loans, and tracking amortization and bank treasury operations.

---

## Features

-  Client management (add/view clients)
-  Loan management (add/view loans)
-  Amortization schedule per loan
-  Bank treasury overview with payment application
-  Secure with `session`-based state storage for isolation per user
-  Dockerized application with automated deployment
-  Styled with Bootstrap for responsive UI
-  Hosted on AWS Elastic Beanstalk via ECR and S3

---

## Prerequisites

Before running or deploying the project, make sure the following tools are installed:

### For local development

- [Python 3.8+](https://www.python.org/downloads/)
- [pip](https://pip.pypa.io/en/stable/installation/)
- [Git](https://git-scm.com/downloads)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [Visual Studio Code](https://code.visualstudio.com/)
- `zip` command (required for packaging `Dockerrun.aws.json`)
  - On Windows, install with:
    ```bash
    winget install --id=GnuWin32.Zip
    ```
  - Or manually download and add to `PATH`
- (Optional)  [winget](https://learn.microsoft.com/en-us/windows/package-manager/winget/) for installing CLI tools

### For deployment (AWS Academy environment)

- AWS CLI (configured with `aws configure`)\
  Go to "C:\Users\\\\.aws\credentials" and paste the data from \
  AWS academy session's details. {aws\_access\_key\_id, aws\_secret\_access, aws\_session\_token}

   
- AWS services used:
  - ECR (Elastic Container Registry)
  - S3 Bucket (for ZIP file upload)
  - Elastic Beanstalk (Docker solution stack)

---

## Project Structure

```
DevOps-Midterm-Project/
├── Docker file/
│   └── Dockerfile
├── Pythoncode/
│   ├── __pycache__/
│   ├── functions.py
│   └── main.py
├── Website/
│   ├── static/
│   │   ├── bootstrap/
│   │   │   ├── css/
│   │   │   └── js/
│   │   └── styles.css
│   ├── templates/
│   │   ├── index.html
│   │   ├── clients.html
│   │   ├── add_client.html
│   │   ├── loans.html
│   │   ├── add_loan.html
│   │   ├── client_detail.html
│   │   ├── amortization.html
│   │   ├── layout.html
│   │   └── bank.html
│   └── app.py
├── .dockerignore
├── Dockerrun.aws.json
├── app-deploy.zip
├── deploy.sh
├── delete.sh
└── README.md
```

---

## How to Run Locally

1. Clone the repository:

   ```bash
   git clone https://github.com/IliaMaks/MidProject.git
   cd MidProject
   ```

2. Install dependencies:

   ```bash
   pip install flask
   ```

3. Run the app:

   ```bash
   python Website/app.py
   ```

4. Open your browser at: [http://localhost:5000](http://localhost:5000)

---

## Run in Docker (Locally)

1. Make sure Docker Desktop is running
2. Build and run the container:
   ```bash
   docker build -t bankloan -f "Docker file/Dockerfile" .
   docker run -p 5000:80 bankloan
   ```
3. Visit: [http://localhost:5000](http://localhost:5000)

---

## Deployment Instructions

1. Open Git Bash or VS Code Terminal
2. Run the deployment script:
   ```bash
   bash deploy.sh
   ```
3. After deployment, find the Elastic Beanstalk URL in the output table.

---

## Known Limitations

- Stateless architecture between instances (session used for state)
- No persistent database (in-memory only)
- Meant for educational/demo use, not production

---


