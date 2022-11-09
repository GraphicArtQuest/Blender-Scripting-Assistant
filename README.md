# Blender Scripting Assistant

<div align="center">

[![An add-on for Blender, at least version 3.3](https://img.shields.io/badge/Blender->3.3-brightgreen?logo=blender&labelColor=white)](https://www.blender.org/)
[![Licensed under the GPL version 3.0](https://img.shields.io/github/license/GraphicArtQuest/Blender-Scripting-Assistant?color=blue)][license]


[![Maintained](https://img.shields.io/badge/Maintained%3F-Yes-brightgreen.svg)][maintainer]
[![Contributions welcome](https://img.shields.io/badge/Contributions-Welcome-brightgreen.svg?style=flat)](CONTRIBUTING.md)

</div>

# Purpose

This Blender add-on provides a suite of tools that makes it easier for developers and artists to easily create other Blender add-ons.

## Key Features

- A debugging server to connect Blender to external code editors (such as VS Code)
- A hot swap system that monitors files and folders for changes and immediately reloads the modified module into Blender

## Long Term Goal

I want to build this project into the defacto tool for Blender add-on developers to use while making and debugging their own scripts and add-ons.

Ultimately, I aim to have this project included as a [community add-on](https://wiki.blender.org/wiki/Process/Addons) bundled with a future Blender release version. 

## History

This add-on is a diverging fork from Alan North's [Blender Debugger for VS Code v2.2.0](https://github.com/AlansCodeLog/blender-debugger-for-vscode). This project expanded beyond Alan's original intent and desire to maintain. I owe many thanks to him for all of his hard work getting the debugging code working after reviewing this [Blender Developer's blog post](https://code.blender.org/2015/10/debugging-python-code-with-pycharm/) about connecting to PyCharm.

<!-- ![Image Showing VS Code side by side with Blender paused at a breakpoint. In the console, a "Debugger is Attached" Statement is printed.](./Example.png) -->

# Getting Started

## Overview
To use this add-on in your workflow, you require the following installed on your computer:

1. The minimum supported [Blender release](https://www.blender.org/download/lts/) or later
1. [Python 3.10](https://www.python.org/downloads/) or later, with PIP

Suggested Additions:

1. The external code editor [Visual Studio Code](https://code.visualstudio.com/download)
1. The [Python Extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python) for VS Code
1. The [`fake-bpy-module`](https://github.com/nutti/fake-bpy-module) package installed by PIP

<!-- I have made a video (click the image below) for those who just started messing with python in Blender or programming in general, but if you're semi-familiar with Python, VS Code, and the command line the following should make sense. If you have any questions or suggestions, don't hesitate to file an issue. -->

<!-- <p align="center" style="position:relative;">
	<a href="https://www.youtube.com/watch?v=UVDf2VSmRvk" title="Click to go to Video">
		<img alt="youtube video" src="https://img.youtube.com/vi/UVDf2VSmRvk/maxresdefault.jpg" height="300" style="margin:0 auto;" />
	</a>
</p> -->

<!-- ## Note on Downloading

**You must down it with the the green `Clone or Download` button above. DO NOT download it from releases!**

This is because blender has a problem with the periods in the name from the version number. It used to be you could rename the zip, but this no longer works, you'll get an error when you try to enable the addon. The onyl fix is to go where the addon was installed and rename the folder there. -->

## Installing Python and Getting Debugpy

Install Python 3 with PIP and check add to PATH.

- If you already have python installed and you can run it from the command line (aka PATH is set), the addon should find it. It checks `where python` or `whereis python` or `which python` to try and determine where python is and uses the first path given<sup id="n2">[2](#f2)</sup>.
- If you are using something like Conda and want to use a virtual environment, to have the addon auto-detect the path you can: activate the environment, run Blender from the command line, and it should work.

	```
	pip install debugpy
	```

- For Visual Studio, the debugpy version that works depends on the Visual Studio version. I have never used Visual Studio, but you can find more info on setting everything up here: [Remotely Debugging Python Code on Linux](https://docs.microsoft.com/en-us/visualstudio/python/debugging-python-code-on-remote-linux-machines#connection-troubleshooting). (it is not Linux specific)

## Setting up this Addon

Install the addon.

If it did not find the path it'll say "debugpy not found", you'll have to set it manually. It's wherever python is + "\lib\site-packages". NO trailing backslash.

If you want, increase the timeout for the confirmation. It'll print "Waiting..." in the console every second until it prints it's timedout. This does not mean the server has timed out *just* the confirmation listener.

Note: you can only start the server once. You cannot stop it, at least from what I understand. If you run it again it'll just tell you it's already running and start the timer again to check for a confirmation.

## Connecting the Editor

Open your addon folder (e.g. "C:\Code\Blender Stuff\addons\myaddon").

Install the Python extension for VS Code if you haven't already. For Visual Studio see [Installing Python Support](https://docs.microsoft.com/en-us/visualstudio/python/installing-python-support-in-visual-studio).

In the lower left, [VS Code should have auto detected](https://code.visualstudio.com/docs/python/python-tutorial#_prerequisites) your Python install and set it as the interpreter. For Visual Studio see [Managing Python Environments](https://docs.microsoft.com/en-us/visualstudio/python/managing-python-environments-in-visual-studio).

Go to the Debugging tab and add a configuration. Pick Python. You'll want the configuration that looks like this, no need to change the defaults, you can delete the rest.

```JSON
{
	"name": "Python: Attach",
	"type": "python",
	"request": "attach",
	"port": 5678,
	"host": "localhost"
}
```

Now when you run the debugger with this config in Blender and VS Code the console should print "Debugger is Attached" if it was still waiting (it should still attach even if it wasn't, it just won't tell you).

## How to Use

At this point you should be able to add a breakpoint and when you trigger it in Blender, Blender should freeze and VS Code should pause on the breakpoint.

After enabling the add-on, you can control the options by using the new "Scripting Assistant" tab in the viewport's N-panel.

Press `Toggle Terminal` to see the output messages.

Start the debug server by pressing "Start Debug Server".

Start or stop monitoring by pressing "Start/Stop Monitoring".

Adjust the settings for these in the drop down menus.

## Advanced Usage

### Wait for Client

The debugger can be made to wait for a client to connect (this will pause all execution). This can be useful for debugging the connection or when running blender headless / in background mode.

To do so, call the server connect command from the python console or from a script/addon like so:

```python
bpy.ops.debug.connect_debugger_vscode(waitForClient=True)
```

#### Running in Headless Mode

First make sure the addon is installed, enabled, and works when you run blender normally.

Blender can then be run in background mode with the `-b/--background` switch (e.g. `blender --background`, `blender --background --python your_script.py`).

See [Blender Command Line](https://docs.blender.org/manual/en/latest/advanced/command_line/introduction.html).

You can detect when blender is run in background/headless mode and make the debugger pause and wait for a connection in your script/addon:

```python
if bpy.app.background:
	bpy.ops.debug.connect_debugger_vscode(waitForClient=True)
```

This will wait for a connection to be made to the debugging server. Once this is established, the script will continue executing and VSCode should pause on breakpoints that have been triggered.

For addons, you will need to do this from a handler:

```python
from bpy.app.handlers import persistent
#...
def register():
   bpy.app.handlers.load_post.append(load_handler)
#...
@persistent
def load_handler(dummy):
	# remove handler so it only runs once
   bpy.app.handlers.load_post.remove(load_handler)
   if bpy.app.background:
      bpy.ops.debug.connect_debugger_vscode(waitForClient=True)

```
See [Application Handlers](https://docs.blender.org/api/current/bpy.app.handlers.html)

### Debugging/Editing Source Code

It is possible to edit the Blender source code but it can be a bit tricky to get it to detect changes (nevermind live editing is buggy anyways).

From blender you can right click just about anything and click "Edit Source" to get it in the text editor. Then to find the path of the file, go to `Text > Save As` and copy it from there.

Open the file in VS Code, connect to the debugging server, make a change and save it.

Now in Blender the text editor will show this little red button in the top left. Click that and reload the file. Then in `Text Editor > Properties` turn on `Live Edit` if you haven't already. Now to actually get Blender to detect any changes you made just type a single character (like add a space anywhere) and *then* it will detect your changes.

### Debugging/Editing Scripts

To use breakpoints and debug, you must open the script where Blender installed it to.

    C:\Users\<user name>\AppData\Roaming\Blender Foundation\Blender\<version>\scripts\addons

# Troubleshooting

- Check you installed the correct debugpy version. With VS Code this should no longer be an issue, but I believe different versions of Visual Studio need different versions of debugpy (see [Installing Python Support](https://docs.microsoft.com/en-us/visualstudio/python/installing-python-support-in-visual-studio)).
- To determine whether the problem is on Blender's side or your editor's: Close Blender and the [testdebugpy test script](https://github.com/GraphicArtQuest/Blender-Scripting-Assistant/blob/main/testdebugpy.py).

```bash
python testdebugpy.py
```

Then, try to connect to the server with your editor. If you're still getting problems then the problem is with VS Code. Try:
- Check your detected your Python install, or set it manually.
- For VS Code try reinstalling the VS Code Python extension.
- Check that VS Code's Python extension is running on the same port in `launch.json` as the debug server port in Blender.

Otherwise, if none of that helped, don't hesitate to file an issue.

# Support Policy

This add-on is maintained and supported. Submit a [bug report][bugs] if you encounter errors.

## Tested

[![An add-on for Blender, at least version 3.3](https://img.shields.io/badge/Blender->3.3-brightgreen?logo=blender&labelColor=white)](https://www.blender.org/)

![Windows Supported](https://img.shields.io/badge/Windows-0078D6?style=for-the-badge=flat&logo=windows&logoColor=white)

## Help Wanted
This add-on should work on MacOS and Linux, but help is required to verify. 

![Mac Supported](https://img.shields.io/badge/Mac-000000?style=for-the-badge=flat&logo=apple&logoColor=white)
![Linux Supported](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge=flat&logo=linux&logoColor=black)
# License and Development

To help as many fellow artists and developers as possible, **Blender Scripting Assistant** and all other files in this repository are distributed as free and open-source software under the [GPL v3.0 License][license], © 2022.

Both [contributions](CONTRIBUTING.md) and [bug reports][bugs] welcome.

If you find this project useful, please leave a :star2: and subscribe to the Graphic Art Quest YouTube channel for more tutorials and 3D art adventures!

[![Subscribe to the Graphic Art Quest YouTube channel](https://img.shields.io/badge/Subscribe%20to%20Graphic%20Art%20Quest-FF0000?style=plastic&logo=youtube&logoColor=white)][subscribe]

# Contact

Maintained by [M. Scott Lassiter][maintainer].


[![GitHub Badge Profile](https://img.shields.io/badge/GitHub-100000?style=plastic&logo=github&logoColor=white)](https://github.com/M-Scott-Lassiter)
[![Twitter Badge Profile](https://img.shields.io/badge/Twitter-1DA1F2?style=plastic&logo=twitter&logoColor=white)](https://twitter.com/MScottLassiter)
[![LinkedIn Badge Profile](https://img.shields.io/badge/LinkedIn-0077B5?style=plastic&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/mscottlassiter)
[![Stackoverflow Badge Profile](https://img.shields.io/badge/stackoverflow-orange.svg?longCache=true&style=plastic&logo=stackoverflow&logoColor=white)](https://stackoverflow.com/users/6186333/sandpiper)

[license]: LICENSE.txt
[bugs]: https://github.com/GraphicArtQuest/Blender-Scripting-Assistant/issues/new/choose
[maintainer]: https://graphicartquest.com/author/scott-lassiter/
[subscribe]: https://www.youtube.com/channel/UCFYKeFMbQnY5CdzFH62PAhg?sub_confirmation=1