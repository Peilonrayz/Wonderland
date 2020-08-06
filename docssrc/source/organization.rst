Organization
============

There are two linked sections of the question organization.
There is the `structure in RST / Website form <rules/index.html>`_.
And the tags applied to questions.

..  warning::

    This is an alpha product, both schemes are the *best so far*.
    They are subject to change.

    | I have plans on removing the Stack Exchange category and merging all rules in with the other categories.
    | Tags will also lose their prefixes at a later date.

Structure
---------

The structure is mostly two or three levels big, depending on how many posts are contained in a group. (rule, sub-rule or sub-sub-rule)
The structure can be expressed as a path in a tree:

..  code::

    {category}    > {rule}             > {sub rule}   > {sub sub rule}

For example:

..  code::

    Close Reasons > Broken             > Bugs (Known) > Troubleshooting
    Site Policy   > Comparative Review
    Privileges    > Questions          > Accept

Category
    These categorize the rules, not the questions.
    For example Broken is a Close Reason rule.
    But we have questions about Site Policy that fall under this this Close Reason rule.
    Take :post:`8394`.

Rule
    These are rules.
    Quite a few will be familiar.
    I add new rules if there are enough questions in the other group that are similar enough.
    
    The names are mostly non-standard.

Sub Rule
    When a rule has hundreds of questions it can help to categorize these in ways they are similar.

Tags
----

At first I'd planned for my tagging scheme to be compatible with Code Review's, however I no longer have that as a goal.
My scheme has 3 required tags meaning any rules that have sub sub rules (2 more tags) can't be red-tagged (featured, etc) on Code Review.
I think this is fine as only I probably care about my tags.
Nor do I have a desire to fight against the status quo.

There are three required tags:

Stack Exchange required tags
    :mtag:`discussion`, :mtag:`feature-request`, :mtag:`bug`, :mtag:`support`.

Question type
    | These are prefixed with :mtag:`t-` and are question specific categories.
    | :mtag:`t-scope`, :mtag:`t-policy`, :mtag:`t-stack-exchange`

Rules
    These are exactly the same as structure's rules. These are prefixed with :mtag:`c-`.

Questions can be tagged with two rules. Tags after this are prefixed with :mtag:`s-` except :mtag:`x-moderation`.

..  note::

    It should be quite apparent that the names are a mess.
    Additionally the prefixes are not here forever and are to help prevent name collisions.

Linking the two systems together
--------------------------------

I am in the process of migrating from having questions grouped and sorted manually in RST to the tag based system. Questions will have tags assigned in the tags.csv file in the top level of the repository. From here I wrote a simple Sphinx directive to grab all tags that match a query and output them into the document as required.

For example the Authorship page is generated completely from the tags file.

..  code:: rst

    Authorship
    ==========

    Legal
    -----

    :tag_group:`c-authorship,s-legal`

    Maintainer
    ----------

    :tag_group:`c-authorship,s-maintainer`

    Other
    -----

    :tag_group:`c-authorship,!s-legal,!s-maintainer`
