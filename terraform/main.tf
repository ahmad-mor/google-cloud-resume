terraform {
  required_version = ">= 1.5.0"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  credentials = file("credentials.json")
  project     = var.project_id
  region      = var.region
}
# 1. تفعيل الـ APIs المطلوبة تلقائياً
resource "google_project_service" "services" {
  for_each = toset([
    "run.googleapis.com",
    "firestore.googleapis.com",
    "cloudresourcemanager.googleapis.com"
  ])
  service            = each.key
  disable_on_destroy = false
}

# 2. إنشاء قاعدة بيانات Firestore (fire123)
resource "google_firestore_database" "database" {
  project     = var.project_id
  name        = var.database_id
  location_id = var.region
  type        = "FIRESTORE_NATIVE"

  depends_on = [google_project_service.services]
}

# 3. إنشاء المستند الأولي للعداد في Firestore
resource "google_firestore_document" "visitor_counter" {
  project     = var.project_id
  database    = google_firestore_database.database.name
  collection  = "voters"
  document_id = "status"
  fields      = "{\"count\":{\"integerValue\":\"0\"}}"
}

# 4. نشر خدمة الـ Backend API على Cloud Run (Function/Python)
resource "google_cloud_run_v2_service" "backend_api" {
  name     = "visitor-counter-api"
  location = var.region
  ingress  = "INGRESS_TRAFFIC_ALL"

  template {
    containers {
      image = "us-docker.pkg.dev/cloudrun/container/hello" # صورة مؤقتة حتى يتم رفع كود الـ Python الخاص بك
      
      env {
        name  = "DATABASE_NAME"
        value = var.database_id
      }
    }
  }

  depends_on = [google_project_service.services]
}

# السماح للعامة بطلب الـ Backend API بدون Authentication
resource "google_cloud_run_v2_service_iam_member" "backend_public_access" {
  project  = var.project_id
  location = var.region
  name     = google_cloud_run_v2_service.backend_api.name
  role     = "roles/run.invoker"
  member   = "allUsers"
}

# 5. نشر خدمة الـ Frontend على Cloud Run (NGINX Container)
resource "google_cloud_run_v2_service" "frontend_web" {
  name     = "cloud-resume"
  location = var.region
  ingress  = "INGRESS_TRAFFIC_ALL"

  template {
    containers {
      image = "us-docker.pkg.dev/cloudrun/container/hello"
    }
  }

  depends_on = [google_project_service.services]
}

# السماح للعامة بفتح الـ Frontend
resource "google_cloud_run_v2_service_iam_member" "frontend_public_access" {
  project  = var.project_id
  location = var.region
  name     = google_cloud_run_v2_service.frontend_web.name
  role     = "roles/run.invoker"
  member   = "allUsers"
}

# 6. ربط الدومين الشخصي (Domain Mapping)
resource "google_cloud_run_domain_mapping" "custom_domain" {
  location = var.region
  name     = var.domain_name

  metadata {
    namespace = var.project_id
  }

  spec {
    route_name = google_cloud_run_v2_service.frontend_web.name
  }
}