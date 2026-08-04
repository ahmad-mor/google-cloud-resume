# ☁️ Google Cloud Platform (GCP) - Cloud Resume Challenge

This repository contains the full-stack codebase and infrastructure configuration for my **Cloud Resume Challenge** deployed on Google Cloud Platform. The project demonstrates a modern serverless architecture, containerization, automated CI/CD pipelines, and cloud security practices.

## 🚀 Live Demo
🌐 **Website:** [https://almorshed.cloud](https://almorshed.cloud)

---

## 🛠️ Architecture & Technologies Used

### 🖥️ Frontend & Containerization
* **NGINX on Google Cloud Run:** Containerized static website served via NGINXAlpine and hosted on serverless GCP Cloud Run.
* **HTML5 / CSS3 / JavaScript:** Clean, responsive design fetching live data dynamically from the backend API.
* **Docker:** Multi-stage image setup configured to listen on port `8080` for Cloud Run compatibility.

### 🌐 Networking, Custom Domain & Security
* **Custom Domain Mapping:** Linked `almorshed.cloud` directly to Cloud Run services.
* **Managed SSL/TLS Certificate:** Automatic HTTPS encryption provisioned via Google Trust Services.
* **DNS Management:** Managed A-records propagation and routing.

### ⚙️ Backend API
* **Cloud Run Functions (Python 3.11):** Serverless HTTP function (`hello_http`) handling visitor requests.
* **CORS Management:** Configured HTTP Headers and Preflight (`OPTIONS`) handling to allow secure cross-origin requests.
* **Transactional Concurrency:** Implemented `@firestore.transactional` logic to accurately increment visitor counters under concurrent loads.

### 🗄️ Database
* **Google Cloud Firestore:** Scalable NoSQL database (`fire123` instance) storing live visitor stats in a `voters/status` collection.

### 🔄 DevOps & CI/CD Pipeline
* **GitHub Actions:** Automated deployment pipeline triggering build and deployment workflows on every `git push` to the `main` branch.
* **Artifact Registry / Container Registry:** Storing and managing Docker container images.

### 🏗️ Infrastructure as Code (IaC)
* **Terraform:** Managed full infrastructure lifecycle using Declarative IaC.
* **Resources Managed:**
  * `google_cloud_run_v2_service` (Frontend NGINX & Backend Python API)
  * `google_firestore_database` & `google_firestore_document` (Database & Schema)
  * `google_cloud_run_domain_mapping` (SSL Certificates & Domain Routing)
  * `google_cloud_run_v2_service_iam_member` (Public Invoker IAM Roles)

---

## 📁 Repository Structure

```text
.
├── Frontend/
│   └── index.html          # Resume frontend markup & JS fetch counter script
├── Dockerfile              # NGINX build instructions & port 8080 configuration
├── main.py                 # Python backend function interacting with Firestore
├── requirements.txt        # Backend dependencies (functions-framework, google-cloud-firestore)
└── README.md               # Project documentation

👨‍💻 Author
Ahmad Abdullah Almorshed

Associate Cloud Engineer (Google Cloud Certified)

GitHub: @ahmad-mor

LinkedIn: linkedin.com/in/ahmad-almorshed