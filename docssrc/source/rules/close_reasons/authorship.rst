Authorship
==========

1.  The asker must be an *author* or *maintainer*, and an *emotional owner* of the code.

    ..  tabs::

        ..  tab:: Hidden
        ..  tab:: Explanation

            -   If the author is not an *author* or *maintainer*;
                the author is unlikely to be able to legally license the code under the current *user contributions license*.

                As a site we don't want to encourage a situation where anyone will seek legal action against users of the site.
    
            -   If the author is not an *emotional owner*;
                the advice we give can be dismissed as someone else's mistake.
                
                As such the site would not be creating the learning environment we want.

        ..  tab:: Examples

            -   ..
                
                    I found some code on the internet; please review the code.
    
        ..  tab:: How to Fix

            The author should rewrite the code from scratch.
            Changing some variable names and reorganizing the code is not allowed.

        ..  tab:: References

            :reference_group:`1`

2.  The asker must license the code under Code Review's current *user contributions license*.

    ..  tabs::

        ..  tab:: Hidden
        ..  tab:: Explanation

            By posting on Code Review you are licensing all contributions under the *user contributions license*.

            If the author don't post the code in the question then we as a site can't review the code.

        ..  tab:: References

            :reference_group:`2`

3.  The asker must understand how the code works.

    ..  tabs::

        ..  tab:: Hidden
        ..  tab:: Explanation
        ..  tab:: Examples
        ..  tab:: How to Fix
        ..  tab:: References

            :reference_group:`3`

4.  The asker must be able to explain how the code works.

    ..  tabs::

        ..  tab:: Hidden
        ..  tab:: Explanation
        ..  tab:: Examples
        ..  tab:: How to Fix
        ..  tab:: References

            :reference_group:`4`

Extra
-----

..  tabs::

    ..  tab:: Hidden
    ..  tab:: Tagged Questions

        **Legal**

        :tag_group:`c-authorship,s-legal`

        **Maintainer**

        :tag_group:`c-authorship,s-maintainer`

        **Other**

        :tag_group:`c-authorship,!s-legal,!s-maintainer`

    ..  tab:: Flow Chart

        .. graphviz::

            digraph {
                {
                    node [shape=ellipse];
                    start [label="Start"];
                    on_topic [label="On-topic"];
                    off_topic [label="Off-topic"];
                }
                {
                    node [shape=diamond, height=1.2];
                    is_author [label="Are you an owner?"];
                    is_illegal [label="Did you post the code?"];
                    is_misunderstand [label="Asking to understand the code?"];
                }
                {
                    node [shape=box];
                    do_rewrite_code [label="Write new code"];
                    do_remove_code [label="Remove the code"];
                }

                {
                    start -> is_author;
                    do_remove_code -> do_rewrite_code;
                    do_rewrite_code -> is_misunderstand;
                }
                {
                    edge [label="yes"];
                    is_author -> is_misunderstand;
                    is_illegal -> do_remove_code;
                    is_misunderstand -> off_topic;
                }
                {
                    edge [label="no"];
                    is_author -> is_illegal;
                    is_illegal -> do_rewrite_code;
                    is_misunderstand -> on_topic;
                }
            }
