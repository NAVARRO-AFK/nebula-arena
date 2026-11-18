variable "cluster_name" {
  description = "Nombre del clúster de kind"
  type        = string
  default     = "nebula"
}

variable "agones_version" {
  description = "Versión del chart de Agones (debe coincidir con la instalada)"
  type        = string
  default     = "1.62.0"
}

variable "namespace_juego" {
  description = "Namespace donde viven las flotas de Nebula Arena"
  type        = string
  default     = "default"
}
