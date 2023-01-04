# filesay

### What is filesay?
This is a program to create a pastebin link for usage with bots like fossabot or streamlabs.
You are able to switch to Dark Mode and Test Mode. It's also possible to activate a "!filesay" prefix for easier use with fossabot or other bots.

### How to use it
First of all you need to create a pastebin account if you dont have one already. Next step is to go to https://www.pastebin.com/doc_api and copy your Developer Api Key. You then need to paste that in the api_dev_key field in the settings.

In the settings you can also enable Dark Mode, Test Mode and the whether or not the program should put "!filesay" before the pastebin link.
All settings are being saved when pressing the "Save" button and you don't need to set them again.

To create a pastebin link you just need to open a csv file in the program, specify the ban reason if wanted and click "Generate Link".
The csv file should be created on https://twitch-tools.rootonline.de/followerlist_viewer.php. These files are tested to work with this program.
You could also use other csv files as long as the username is in the first column or in the only column. Keep in mind that it skips the first line of the csv when you create your own.

Test Mode is a way to test the functionality of the program without wasting one of the pastes on the website. You can just copy it to your clipboard and analyse it.
