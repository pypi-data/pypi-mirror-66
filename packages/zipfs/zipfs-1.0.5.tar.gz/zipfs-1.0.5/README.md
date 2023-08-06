# zipf

CLI tool to directly zip several files/folders or an existing folder

Make a zip from list of files/folders with or without specifying the archive name ("%Y_%m_%d-%H_%M_%S.zip" if not specified) or from an existing folder.


# Installation
```sh
With pip:
sudo pip3 install zipfs

With yay:
yay -a zipf

With yaourt:
yaourt -a zipf
```

# Compatibility
python >= 3


# Usage
<pre>
<b>zipf / zipper</b> [<b>F_PATH_01 F_PATH_02 ...</b>] [<b>ARCHIVE_NAME</b>]
<b>options:</b>
<!-- -->         <b>-h, --help</b>        show this help message and exit
</pre>


# Examples
For **help**:<br/>
```sh
zipf -h
or
rt --help
```

<br/>Make a zip archive from 3 files:<br/>
```sh
zipf titi/toto.jpg titi/tutu.jpg tata.txt
```
Giving the **2019_05_15-17_25_44.zip** archive<br/><br/>

Make a zip archive from 2 files and one folder with specifying the archive name (work):<br/>
```sh
zipf titi/toto.jpg titi/ tata.txt work
```
Giving the **work.zip** archive
