# Please make these obsolete soon

These are literally just some bash scripts I wrote for my own convenience. They
are not at all guaranteed to work. These should be replaced with an actual
interface for klog and then deleted as soon as possible.

You can look at them for what they do (they're not very long) but essentially
they all run the `getlog` script on klog-server (if the klog repository moves)
there this'll break), and then do something with the run ids you select.

`getlog` rsyncs the entire run directory to your current working directory
`getlink` prints the "klog:8000" link to the run you selected (broken for
multi-select)
`getrr` rsyncs the rerun file from the selected run to your current working
directory
