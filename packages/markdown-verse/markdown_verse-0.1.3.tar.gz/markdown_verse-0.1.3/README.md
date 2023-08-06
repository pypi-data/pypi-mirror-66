markdown\_verse
==============

Python Markdown extension for wrapping verse

```markdown
Hello World
===========

'''
Arctic fox's den
adorned with flowers and snow
garden in winter
'''
```

Leads to:

```html
<h1>Hello World</h1>
<p><div class="verse">Arctic fox's den
adorned with flowers and snow
garden in winter</div></p>
```

You can also specify the tags to wrap the verse block:

```python
markdown(source, extensions=[VerseExtension(
    tag_tuple=('<verse>', '</verse>'))])
```

with the above markdown would lead to:

```html
<h1>Hello World</h1>
<p><verse>Arctic fox's den
adorned with flowers and snow
garden in winter</verse></p>
```

Todo
----

Get rid of the errant paragraph tags
