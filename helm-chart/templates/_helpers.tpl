{{/* vim: set filetype=mustache: */}}
{{/*
Expand the name of the chart.
*/}}
{{- define "streams-explorer.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "streams-explorer.fullname" -}}
{{- if .Values.fullnameOverride -}}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" -}}
{{- else -}}
{{- $name := default .Chart.Name .Values.nameOverride -}}
{{- if contains $name .Release.Name -}}
{{- .Release.Name | trunc 63 | trimSuffix "-" -}}
{{- else -}}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}
{{- end -}}
{{- end -}}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "streams-explorer.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "streams-explorer.serviceAccountName" -}}
{{- if and .Values.rbac.create .Values.rbac.useExistingServiceAccount -}}
    {{ default .Values.rbac.useExistingServiceAccount }}
{{ else }}
    {{ default "streams-explorer-sa" }}
{{- end -}}
{{- end -}}

{{- define "streams-explorer.roleName" -}}
{{- if and .Values.rbac.create .Values.rbac.useExistingRole -}}
    {{ default .Values.rbac.useExistingRole }}
{{ else }}
    {{ default "streams-explorer-role" }}
{{- end -}}
{{- end -}}
