# OneNote
Easily manage embedded multiline notes in [Taskwarrior](https://taskwarrior.org)

### Why would you want this?

While Taskwarrior provides a robust system for annotating tasks, using these
to include extensive notes on a task is cumbersome and difficult to edit in my
experience.

There are some third party scripts that associate files with tasks, however
this involves a whole other system that has to be synchronized/maintained,
which seems unnecessary given Taskwarrior's current syncing capabilities.

OneNote manages notes in a custom data field directly in Taskwarrior, and
automatically opens a pipe editor for managing notes efficiently.

### Installation

#### Dependencies

 * Taskwarrior (preferably 2.5.2 or greater)
 * Bash
 * Vipe pipe editor (readily available in the ```moreutils``` package on most platforms)
 * Python (if using the add/modify hooks)

#### Taskwarrior configuration

OneNote expects a ```notes``` UDA to be available for data storage.

Add this to your ```.taskrc``` config file with the following commands:

```
task config uda.notes.type string
task config uda.notes.label Notes
```

#### Script

Place the ```onenote``` script anywhere in your PATH and make sure it's
executable.

#### Add/modify hooks

The optional add/modify hooks manage an annotation related to the existence of
notes on a task in an intelligent fashion:

 * Adds an annotation when a new note is added
 * Updates the annotation entry date if notes are updated
 * Removes the annotation if notes are completely removed

To use the hook, copy or symlink ```manage_notes_annotation.py``` to your
hooks directory, and make sure it's executeable.

 * For the add hook, name it ```on-add-onenote-manage-notes-annotation.py```
 * For the modify hook, name it ```on-modify-onenote-manage-notes-annotation.py```

### Usage

To add/edit notes attached to a task, execute ```onenote <task_id>```, which
automatically opens an editor for the notes.

Upon save/exit of the editor, the new notes are updated on the task.

Vipe, the default pipe editor, opens the note in Vim. You can override this
with your own pipe editor by setting the ```ONENOTE_PIPE_EDITOR``` environment
variable to another pipe editor available in your path.

To remove notes, you can use the procedure above and completely remove all
content in the editor, or for a shortcut modify the
```notes``` attribute directly:

```
task <task_id> modify notes:
```

Notes can also be piped from other processes directly to a task:

```
echo "foo" | onenote <task_id> -
```

**Just be aware this will overwrite any existing notes on the task!**

#### Environment variables

OneNote sets the environment variable ```ONENOTE_TASK``` for the pipe editor
process, the value of which is the task ID/UUID associated with the note.

#### Default note content (optional)

You can configure default content for an empty note by setting the
```ONENOTE_DEFAULT_CONTENT``` environment variable. If OneNote detects that
the opened note is empty, it will insert the configured default content
instead. If the note has any content at all, the default content will not be
added to the note.

This is an extremely handy feature when used with something like Vim's
modelines. For example, the VimOutliner plugin registers the ```votl```
filetype for its outlining functionality. With a Bash alias like this, you can
ensure that the note always contains the correct modeline to activate the
outliner, even if the note was originally empty:

```sh
alias outline="ONENOTE_DEFAULT_CONTENT='# vi: ft=votl' onenote"
```

#### Converting a line in a note to a task (optional)

The included ```vim-line-to-task.sh``` script provides integrated support for
converting a line of text in a note to a task on the same project as the task
that contains the note. For example, to configure the script to work with
Vim/Vipe, add the following to your ```.vimrc```:

```vimrc
nnoremap <silent> <Leader>t :.w !/path/to/vim-line-to-task.sh<CR>
```

The script also has basic support for converting a line of text outside of
OneNote's default editor, in this case it will assign the task to your configured
default project.

### VIT configuration (optional)

If you're using a version of [VIT](https://github.com/vit-project/vit) that
supports map commands, you can easily add a command to open a task's notes via
onenote:

```dosini
# Open OneNote for the current task.
o = :!wr onenote {TASK_UUID}<Enter>
```

Then in VIT, highlighting a task and hitting the ```o``` key will open the
notes editor, and saving will return you to VIT -- pretty convenient!

### Support

The issue tracker for this project is provided to file bug reports, feature
requests, and project tasks -- support requests are not accepted via the issue
tracker. For all support-related issues, including configuration, usage, and
training, consider hiring a competent consultant.

### Unit tests

OneNote has full unit test coverage. They can be run with:

```
cd /path/to/onenote
./run-tests.sh
```

Python >= 2.7 and the [basht](https://github.com/progrium/basht) testing
framework are required.

### Caveats

While it's possible to modify the ```notes``` UDA directly using standard
Taskwarrior syntax, it's not advisable (except in the deletion case), as, by
necessity, multiline UDA fields are stored as a single-line string with newline
separators, which would be pretty tedious to navigate directly.

Because of
[this bug](https://github.com/GothenburgBitFactory/taskwarrior/issues/2107),
in Taskwarrior versions less than 2.5.2, newlines are represented internally by the marker
```###NEWLINE###```. This is not an issue in TaskWarrior versions from 2.5.2 on.
If you use OneNote with a Taskwarrior version less than 2.5.2, then
upgrade to Taskwarrior version 2.5.2 or greater, you can use the
[convert-5.1-to-5.2.sh](convert-5.1-to-5.2.sh) script to upgrade your tasks, but you are
strongly encouraged to run ```convert-5.1-to-5.2.sh --help``` first and read the
instructions -- the script will automatically edit **ALL** of your tasks!
