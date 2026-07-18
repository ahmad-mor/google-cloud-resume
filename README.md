# Google Cloud Platform (GCP) - Cloud Resume Challenge

This repository contains the source code for my Cloud Resume Challenge, demonstrating serverless architecture, CI/CD, and infrastructure deployment on Google Cloud Platform.

## 🚀 Live Demo
You can visit the live website here: [https://almorshed.cloud](https://almorshed.cloud)

## 🛠️ Architecture & Technologies Used

### Frontend
* **Google Cloud Storage:** Hosts the static website (`index.html`).
* **JavaScript:** Embedded script to fetch live visitor data from the backend API.

### Networking & Security
* **Global HTTP(S) Load Balancer:** Configured to route external traffic efficiently.
* **Cloud CDN:** Enabled to cache content globally for faster loading times.
* **SSL/TLS Certificate:** Secured the custom domain (`almorshed.cloud`) via HTTPS.

### Database
* **Google Cloud Firestore:** NoSQL database configured in the `me-central1` (Doha) region to store the live visitor count.

### Backend API
* **Cloud Run Functions:** Serverless API written in **Python 3.12** to handle data increments.
* **CORS Security:** Handled Cross-Origin Resource Sharing to restrict API access strictly to the resume domain.
* **Cloud Firestore Transactions:** Implemented transactional database updates to handle concurrent visitor spikes without data corruption.
* **Identity and Access Management (IAM):** Configured appropriate service account permissions using the `Cloud Datastore User` role for secure database access.
