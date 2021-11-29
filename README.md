# MuBuild

* The build system which is written in under 200 lines.
* It is portable, and powerful.
* It is written in Python, and there is support for Windows/DOS based systems, along with POSIX.

A sample build file is as follows:
```
Define NAME muBuild

// A test MuFile which demonstrates targets and variables

Target _nt Test
    echo Hello &NAME are you having a good day?
End

Target _posix Test
    echo "Hello &NAME are you having a good day?"
End
```

More documentation will be coming soon.<br>
Discord Server for MuTools: https://discord.gg/Zb5MHSBG
