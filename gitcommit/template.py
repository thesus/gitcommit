template = """# Your smart git commit message by igit commmit
{% if message %}
# {{message}}
{% endif %}
{% if remote and remote.next_task %}
{{ remote.next_task }}
{% endif %}
{% if code.changed_funcs or code.added_funcs or code.removed_funcs %}
# Here is the list of changed functions:
{% if code.changed_funcs %}
{% for func in code.changed_funcs %}
Change function '{{func.name}}' in '{{func.filename}}'
{% endfor %}
{% endif %}
{% if code.added_funcs %}
{% for func in code.added_funcs %}
Add function '{{func.name}}' in '{{func.filename}}'
{% endfor %}
{% endif %}
{% if code.removed_funcs %}
{% for func in code.removed_funcs %}
Remove function '{{func.name}}' in '{{func.filename}}'
{% endfor %}
{% endif %}
{% endif %}

{% if history %}
# Here is a list with the last commits that changed the same file(s):
{% for commit in history %}
#- ({{ commit.author }}) {{ commit.message }}
{% endfor %}
{% endif %}
"""
