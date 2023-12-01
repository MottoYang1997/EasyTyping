# EasyTyping

## What's EasyTyping

A simplified notepad to help you stay motivated and focused on writing tasks with the following methods:

1. Immediate feedback on your progress. As you started typing, the notepad will count your words and update the progress bar as a hint on how far you have started from doing nothing at all.
1. Negative prompt when you are idling. When you have paused for 3 seconds and the progress bar has not been completed yet, the typed words will fade out gradually to push you back into writing. When the text is completely blank, the notepad will fail this typing challenge, cut what you have typed into clipboard, and clear text area.
1. When you have typed enough words and the progress bar is finished. This means you have made a good start towards finishing the writing task. The notepad will end the negative prompts until you have opened a blank page or cleared out the text.
1. The notepad also provides a thesaurus dictionary and motivation wizard. The wizard can help you know your feelings and clear out the potential benefits of the task even if you don't want to do it.

## Functionality

1. Instant positive and negative feedback on your writing progress.
1. Thesaurus Dictionary.
1. Motivation Wizard.
1. Real-time Markdown Rendering through `mistletoe`

## How to run this software

1. Install the latest [Python 3](https://www.python.org/downloads/)
2. In the commandline prompt, type
~~~
pip install pyqt6 requests pyqt6-webengine mistletoe
~~~
3. In the project root folder, type
~~~
python main_window.pyw
~~~

## Note

1. To use the thesaurus dictionary, please register an API key at [API Ninjas](https://api-ninjas.com/api/thesaurus).

1. The software depends on the followign libraries.
    1. PyQt6
    1. requests
    1. mistletoe

## TODO
1. Rewrite the MainWindows class to decouple the open, save, save as operations.
1. Implement a state machine to track the status of the document. (Changed, unchanged, etc)
1. Add a setting dialog to configure the writing feedback.

## Acknoledgement

The development of this software has referred to the following libraries and websites.

1. [PyQt6](https://www.riverbankcomputing.com/software/pyqt/)
1. [Microns Icon Library](https://www.s-ings.com/projects/microns-icon-font/)
1. [QFindDialogs](https://github.com/Yet-Zio/QFindDialogs)
1. [How to Motivate Yourself to Do Things You Don't Want to Do - HBR](https://hbr.org/2018/12/how-to-motivate-yourself-to-do-things-you-dont-want-to-do)
1. [Thesaurus API](https://api-ninjas.com/api/thesaurus)
1. [The most dangerous writing app](https://www.squibler.io/dangerous-writing-prompt-app)
1. [Mistletoe python markdown render](https://github.com/miyuchina/mistletoe)
