======
Cowork
======


TODO
====

- Need to run a separate server, (e.g. jupyter dash comments dot com)
  - Need to test: using external server, can notebooks rendered on GitHub show comments?
  - Server running in the notebook needs access to database (for local development)
  - Users can run their own server or use public one (free for open source?)
  - Allow users to run their own server.
- Rename to jupyter-comments (module name jupyter_comments)
- Support deleting comments
- Support editing comments
- Render comment message as markdown
- Option to render comments when notebook is converted to HTML?
- Strip the <head> from the comments embedded in voila page
- How to mention people?
  - Use "@gjenks" like Slack
- Add /manage type endpoint/function for viewing all documents/topics


Example
=======

.. code-block:: python

   import cowork

   cowork.setup(
       'Latency-Analysis',
       database='sqlite3:///tmp/Latency-Analysis.sqlite3',
   )
   # Initialize database
   # Start the WSGI server in the background (Tornado)
   cowork.comments('Histogram-Code-Review-Latency')
   # Emit Javascript that polls server for comments


Ideas
=====


Google Docs
...........

- How to be like Google Docs?
  - Idea: two-way data binding with Google Docs.
    - Copy images to Google Doc and support syncing.
- Converting to HTML, uploading to Drive, and then opening with Docs did not work.
  - $ jupyter nbconvert --to html --no-input --no-prompt Test-Analysis.ipynb
  - But copy/paste from web page to Docs works.
    - But replacing all content will remove comments from others.
- How to upload image through Docs API?


Slack
.....

- https://api.slack.com/rtm
- Looks complicated and I can't develop locally :(


Isso
....

- https://github.com/posativ/isso
- $ pipx install isso
- $ isso -c isso.cfg run

.. code-block:: python

   from IPython.core.display import HTML
   script = '''
   <script data-isso="//localhost:8080/"
           data-isso-reply-to-self="true"
           data-isso-require-author="false"
           data-isso-require-email="false"
           data-isso-avatar="false"
           src="//localhost:8080/js/embed.min.js"></script>
   <section id="isso-thread"></section>
   '''
   HTML(script)
