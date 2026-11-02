{{- $entries := slice -}}
{{- range site.Pages -}}
  {{- $path := slice -}}
  {{- range .Ancestors.Reverse -}}
    {{- if not .IsHome -}}{{- $path = $path | append .Title -}}{{- end -}}
  {{- end -}}
  {{- /* One entry per heading: the page's list of children is left out, and each heading becomes a marker to split on. */ -}}
  {{- $html := .Content | replaceRE `(?s)<nav class="pages">.*?</nav>` "" | replaceRE `(?s)<h[1-6] id="([^"]+)">(.*?)<a class="anchor".*?</h[1-6]>` "\x1f${1}\x1e${2}\x1e" -}}
  {{- $sections := slice -}}
  {{- range $i, $part := split $html "\x1f" -}}
    {{- $id := "" -}}{{- $heading := "" -}}{{- $body := $part -}}
    {{- if $i -}}
      {{- $bits := split $part "\x1e" -}}
      {{- $id = index $bits 0 -}}
      {{- $heading = index $bits 1 | plainify | htmlUnescape -}}
      {{- $body = index $bits 2 -}}
    {{- end -}}
    {{- $text := $body | plainify | htmlUnescape | replaceRE "[‘’]" "'" | replaceRE "[“”]" "\"" | replaceRE `\s+` " " | strings.TrimSpace -}}
    {{- $sections = $sections | append (dict "i" $id "h" $heading "x" $text) -}}
  {{- end -}}
  {{- $entries = $entries | append (dict "t" .Title "u" (strings.TrimPrefix "/" .RelPermalink) "p" $path "s" $sections) -}}
{{- end -}}
window.searchIndex = {{ $entries | jsonify }};
