We have created a custom renderer that can render markdown to Slack blocks. @slack_blocks_renderer.py

The Slack blocks are defined in the slack_sdk and you can see them in the @.venv/lib/python3.13/site-packages/slack_sdk/models/blocks folder.

We use mistletoe python package to parse the markdown. It has `BaseRenderer` class that we can inherit from to create a custom renderer.
You can see example implementations in the @.venv/lib/python3.13/site-packages/mistletoe/contrib folder, where you can understand how the renderer implementation works.

Our renderer returns a list of `Block` objects.