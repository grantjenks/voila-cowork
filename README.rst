* README
  - Interesting: https://docs.microsoft.com/en-us/graph/auth-register-app-v2
** Voila
   - Helpful to see comments rendered in both Voila and Jupyter.
   - $ voila .
   - TODO:
     - How to handle authentication?
     - How to mention people?
     - Create comments / delete comments?
```
import coms
coms.initialize('NSAT-Analysis')
# Initialize SQLite database
# And start server in background (Tornado)
...
coms.comments('NSAT-Response-vs-MP')
# Emit Javascript that polls server for comments.
```
** Google Docs?
   - How to be like Google Docs?
     - Idea: two-way data binding with Google Docs.
       - Copy images to Google Doc and support syncing.
   - Converting to HTML, uploading to Drive, and then opening with Docs did not work.
     - $ jupyter nbconvert --to html --no-input --no-prompt Test-Analysis.ipynb
     - But copy/paste from web page to Docs works.
       - But replacing all content will remove comments from others.
   - How to upload image through Docs API?
** Embed Slack
   - https://api.slack.com/rtm
   - Looks complicated and I can't develop locally :(
** Use "Isso"
   - https://github.com/posativ/isso
   - $ pipx install isso
   - $ isso -c isso.cfg run
```
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
```
