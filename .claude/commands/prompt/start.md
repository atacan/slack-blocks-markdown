We want to create a custom renderer that can render markdown to Slack blocks.

The Slack blocks are defined in the slack_sdk and you can see them in the @.venv/lib/python3.13/site-packages/slack_sdk/models/blocks folder.

We use mistletoe to parse the markdown. It has `BaseRenderer` class that we can inherit from to create a custom renderer.
You can see example implementations in the @.venv/lib/python3.13/site-packages/mistletoe/contrib folder, where you can understand how the renderer implementation works.

Our renderer should return a list of `Block` objects.

You can create as many files as you want. To test the renderer, you can output the JSON representation of the blocks to a file from a development script, so that I can check it in Slack's block kit builder web interface.