resource "kubernetes_manifest" "fleet" {
  manifest = {
    apiVersion = "agones.dev/v1"
    kind       = "Fleet"
    metadata = {
      name      = "nebula-fleet"
      namespace = var.namespace_juego
    }
    spec = {
      replicas = 3
      template = {
        spec = {
          ports = [
            { name = "game", containerPort = 7654, protocol = "TCP" }
          ]
          health = { initialDelaySeconds = 10, periodSeconds = 5 }
          template = {
            spec = {
              containers = [{
                name            = "nebula"
                image           = "nebula-server:1.0"
                imagePullPolicy = "IfNotPresent"
                ports           = [{ name = "metrics", containerPort = 9100 }]
                resources = {
                  requests = { cpu = "250m", memory = "256Mi" }
                  limits   = { cpu = "500m", memory = "512Mi" }
                }
              }]
            }
          }
        }
      }
    }
  }
  depends_on = [helm_release.agones]
}

resource "kubernetes_manifest" "autoscaler" {
  manifest = {
    apiVersion = "autoscaling.agones.dev/v1"
    kind       = "FleetAutoscaler"
    metadata = {
      name      = "nebula-autoscaler"
      namespace = var.namespace_juego
    }
    spec = {
      fleetName = "nebula-fleet"
      policy = {
        type   = "Buffer"
        buffer = { bufferSize = "20%", minReplicas = 3, maxReplicas = 10 }
      }
    }
  }
  depends_on = [kubernetes_manifest.fleet]
}
