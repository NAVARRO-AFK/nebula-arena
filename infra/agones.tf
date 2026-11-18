resource "helm_release" "agones" {
  name             = "agones"
  repository       = "https://agones.dev/chart/stable"
  chart            = "agones"
  version          = var.agones_version
  namespace        = "agones-system"
  create_namespace = false
  wait             = false
}
