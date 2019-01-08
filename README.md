# Check_mk notifications in Matrix

This scripts gives your Check_mk installation a possibility to send notifications into [Matrix](https://matrix.org) chatroom.

## Installation

To install this script do the following:

1. Copy matrix.py file contents into clipboard.
2. Execute ``omd su SITENAME``, where ``SITENAME`` is a site name for OMD. If you're using check_mk installed from source - skip this step.
3. Open ``~/local/share/check_mk/notifications/matrix.py`` for editing and paste ``matrix.py`` file contents into it. Make it executable (``chmod +x ~/local/share/check_mk/notifications/matrix.py``). Check_mk installed from source can place it's files somewhere else and admins of these installations should figure out by themselves where to put this file.

### Dependencies

This script has no dependencies except Python 3. It was written specifically to be very compact and understandable.

## Configuration

This script will send notifications as user, so you should create a separate user for it. Consult your homeserver's documentation about instructions.

You'll need these parameters:

* Homeserver URL - this is what you're specifying in Riot and other clients.
* Notification bot user's token. To get it log in as created user, tap on settings icon in bottom left part of Riot and scroll in the very end.
* Room ID. It's available in room settings.

After obtaining all of them you should create new notification with parameters like this:

![Check_mk notifications configuration](/check_mk_notifications_configuration.png)

Where 1st parameter is a homeserver URL (with http or https), second parameter is a bot user's access token and third parameter is a room ID.