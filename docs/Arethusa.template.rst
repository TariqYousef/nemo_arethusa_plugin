Text Template and It's Macro
============================

The :code:`arethusa::text.html` contains few macro to ensure reusability of the concept by other resources :

tb_macro()
##########

Contains the container for the Arethusa Widget

tabs(text, treebank)
####################

Creates a Bootstrap tab interface where the first tab is the text, the second would be the treebank

Blocks and extensions
#####################

- The template extends main::container.html and feeds blocks additinalscript and article.
- It imports from :code:`main::text.html` : :code:`show_passage`, :code:`header_passage`, :code:`default_footer`, and :code:`nav`