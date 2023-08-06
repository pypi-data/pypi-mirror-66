A simple list making utility.

This command line utility makes it easy to manage hierarchical lists. You can
have any number of lists with any number of sub-lists and keep repeating this
to any depth you choose. Note that this is primary meant for use by humans and
will perform poorly if used for large lists created or read by automatons.

The utility follows a modal approach like Vim to make input commands simple.
While in normal mode, you can navigate around the document. When in Edit mode
you can add or edit text.

At this stage, the utility is quite barebones and is missing a fair bit of
functionality. I consider it the bare minimum of what's usable. The following
features are supported:
- Editing text
- Saving file
- Adding child nodes
- Adding sibling nodes
- Deleting nodes

Essential features that are *not yet implemented*:
- Scrolling (yes, I'm sorry! very high on list to fix)
- Undo
- Not saved warning
- Move nodes from one parent to another.
- Indent/unindent nodes
- Resizing terminal window
- Copy/paste
- Collapsing/expanding sub-lists.

Features to be implemented down the road:
- Zooming in and out of sub-lists.
- Adding detailed text to nodes
- Tagging nodes with keywords for searching

