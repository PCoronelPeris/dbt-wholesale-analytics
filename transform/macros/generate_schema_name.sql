{# Renders schemas as {target.name}_{custom_schema_name}, for example dev_marts #}
{% macro generate_schema_name(custom_schema_name, node) -%}
    {%- if custom_schema_name is none -%}
        {{ target.schema }}
    {%- else -%}
        {{ target.name }}_{{ custom_schema_name | trim }}
    {%- endif -%}
{%- endmacro %}
