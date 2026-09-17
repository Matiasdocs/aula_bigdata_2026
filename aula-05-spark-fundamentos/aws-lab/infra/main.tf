# main.tf — aws-lab (aula-05: Spark/RDDs no AWS Glue)
# =============================================================================
# ADAPTADO: o bucket S3 e os arquivos (script + dado de entrada) já foram
# criados/enviados manualmente via AWS CLI, pois a política do Learner Lab
# bloqueia a checagem de Object Lock que o Terraform tenta fazer ao gerenciar
# um bucket S3 diretamente (s3:GetBucketObjectLockConfiguration com "explicit
# deny"). O Terraform aqui cuida apenas do AWS Glue Job, que não sofre esse
# bloqueio.
# =============================================================================

provider "aws" {
  region = var.regiao

  default_tags {
    tags = var.tags
  }
}

# -----------------------------------------------------------------------------
# AWS Glue Job (glueetl) — o motor onde os RDDs vão rodar.
# Não há cluster para ligar/desligar: driver e executors são provisionados
# sob demanda quando o job é disparado (aws glue start-job-run) e liberados no
# fim. NÃO cria IAM role: usa a LabRole por ARN (var.labrole_arn).
# -----------------------------------------------------------------------------
resource "aws_glue_job" "wordcount" {
  name     = "job-aula05-wordcount"
  role_arn = var.labrole_arn

  glue_version      = "4.0"
  worker_type       = "G.1X"
  number_of_workers = 2

  command {
    name            = "glueetl"
    python_version  = "3"
    script_location = "s3://${var.bucket_nome}/scripts/rdd_job.py"
  }

  default_arguments = {
    "--INPUT"  = "s3://${var.bucket_nome}/input/sample_lines.txt"
    "--OUTPUT" = "s3://${var.bucket_nome}/output/wordcount"
    "--enable-continuous-cloudwatch-log" = "true"
    "--TempDir" = "s3://${var.bucket_nome}/tmp/"
  }
}