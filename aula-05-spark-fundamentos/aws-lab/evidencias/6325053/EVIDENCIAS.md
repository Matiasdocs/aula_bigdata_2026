# Evidências — Lab Aula 05 (Spark RDDs na AWS)

## Identificação

- **Nome:** Matheus Gabriel Correa Braga Viana
- **RA:** 6325053
- **Branch:** aula-05-aws-6325053
- **Data:** 17/09/2026

---

## 1. Identidade AWS ativa

```bash
aws sts get-caller-identity
```

```text
{
    "UserId": "AROAQHJJMUQE6644YXJHU:user5367795=Gabriel_Viana_-_6325053",
    "Account": "015656068105",
    "Arn": "arn:aws:sts::015656068105:assumed-role/voclabs/user5367795=Gabriel_Viana_-_6325053"
}
```

---

## 2. `terraform apply` concluído

```text
Plan: 1 to add, 0 to change, 0 to destroy.

aws_glue_job.wordcount: Creating...
aws_glue_job.wordcount: Creation complete after 1s [id=job-aula05-wordcount]

Apply complete! Resources: 1 added, 0 changed, 0 destroyed.

Outputs:

bucket_nome = "lab-aula05-glue-6325053"
glue_job_nome = "job-aula05-wordcount"
labrole_arn = "arn:aws:iam::015656068105:role/LabRole"
```

---

## 3. Job com estado SUCCEEDED

```text
JobRunId: jr_65ca477d6fe30bc23dd01095959c1073627735d8a5506865610bfab66b1a540f
JobRunState: SUCCEEDED
```

---

## 4. Resultado do word count

```text
2026-09-17 16:52:10        311 part-00000
2026-09-17 16:52:10        377 part-00001
2026-09-17 16:52:10        377 part-00002
2026-09-17 16:52:10        394 part-00003

o,60
a,22
e,19
pedido,19
cliente,18
entrega,17
do,16
produto,16
estoque,14
pagamento,11
com,9
de,8
um,7
para,6
cada,5
dia,5
mais,5
que,5
ao,4
foi,4
grande,4
novo,4
pediu,4
da,3
muitos,3
na,3
pedidos,3
pelo,3
voltou,3
```

---

## 5. Top palavras / interpretação

```text
o,60
a,22
e,19
pedido,19
cliente,18
```

> "o", "a" e "e" dominam por serem artigos/conjunções comuns em português. As demais — "pedido", "cliente", "entrega", "produto", "estoque", "pagamento" — indicam um texto sobre ciclo de pedidos de e-commerce.

---

## 6. Logs do driver (opcional / bônus)

Não incluído nesta entrega.

---

## 7. Limpeza (`terraform destroy`)

```text
$ terraform destroy
Plan: 0 to add, 0 to change, 1 to destroy.
aws_glue_job.wordcount: Destroying... [id=job-aula05-wordcount]
aws_glue_job.wordcount: Destruction complete after 0s

Destroy complete! Resources: 1 destroyed.

$ aws s3 rb s3://lab-aula05-glue-6325053 --force
delete: s3://lab-aula05-glue-6325053/input/sample_lines.txt
delete: s3://lab-aula05-glue-6325053/scripts/rdd_job.py
delete: s3://lab-aula05-glue-6325053/output/wordcount/part-00000
delete: s3://lab-aula05-glue-6325053/output/wordcount/part-00001
delete: s3://lab-aula05-glue-6325053/output/wordcount/part-00002
delete: s3://lab-aula05-glue-6325053/output/wordcount/part-00003
remove_bucket: lab-aula05-glue-6325053
```

---

## Checklist de conferência

- [x] 1. Identidade AWS ativa (`aws sts get-caller-identity`)
- [x] 2. `terraform apply` concluído ("Apply complete!" + outputs)
- [x] 3. Job com estado `SUCCEEDED` (Glue) (+ `RUN_ID`)
- [x] 4. Resultado do word count (`./ver_resultado.sh`)
- [x] 5. Top palavras + interpretação (2–3 frases)
- [ ] 6. Logs do driver (opcional / bônus)
- [x] 7. Limpeza com `terraform destroy` ("Destroy complete!")