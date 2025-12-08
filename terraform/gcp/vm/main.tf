provider "google" {
  credentials = file("cli-service-account-key.json")
  project = "playground-s-11-a2cd1da6"
  region = "us-east-1"
}

resource "google_compute_address" "vm_static_ip" {
  name = "debian-vm-static-ip"
  region = "us-east1"
  network_tier = "PREMIUM"
}

resource "google_compute_firewall" "allow_web_traffic" {
  name = "allow-web-traffic"
  network = "default"
  direction = "INGRESS"

  allow {
    protocol = "tcp"
    ports = ["22", "80", "443", "3306"]
  }

  target_tags = ["web-server"]
  source_ranges = ["0.0.0.0/0"]
} 

resource "google_compute_instance" "debian_vm" {
  name = "mysql-test"
  machine_type = "n2-standard-2"
  zone = "us-east1-b"

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-13"
      size = 30
      type = "pd-ssd"
    }
  }

  network_interface {
    network = "default"
    access_config {
      nat_ip = google_compute_address.vm_static_ip.address
    }
  }

  tags = ["web-server"]
} 

output "vm_name" {
    value = google_compute_instance.debian_vm.name
}

output "vm_external_ip" {
    value = google_compute_address.vm_static_ip.address
} 

output "vm_zone" {
  value = google_compute_instance.debian_vm.zone
}