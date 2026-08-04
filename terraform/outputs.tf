output "frontend_url" {
  value       = google_cloud_run_v2_service.frontend_web.uri
  description = "The Cloud Run URL for the Frontend"
}

output "backend_api_url" {
  value       = google_cloud_run_v2_service.backend_api.uri
  description = "The Cloud Run URL for the Backend API"
}

output "domain_mapping_status" {
  value       = google_cloud_run_domain_mapping.custom_domain.status
  description = "Domain mapping resource records and SSL provisioning status"
}