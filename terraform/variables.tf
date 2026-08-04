variable "project_id" {
  description = "The GCP Project ID"
  type        = string
}

variable "region" {
  description = "The primary region for resources"
  type        = string
  default     = "europe-west1"
}

variable "domain_name" {
  description = "Custom domain for the resume"
  type        = string
  default     = "almorshed.cloud"
}

variable "database_id" {
  description = "Firestore Database ID"
  type        = string
  default     = "fire123"
}