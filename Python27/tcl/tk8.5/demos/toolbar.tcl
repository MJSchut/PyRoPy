# toolbar.tcl --
#
# This demonstration script creates a toolbar that can be torn off.
#
# RCS: @(#) $Id: toolbar.tcl,v 1.3 2007/12/13 15:27:07 dgp Exp $

if {![info exists widgetDemo]} {
    error "This script should be run from the \"widget\" demo."
}

package require Tk
package require Ttk

set w .toolbar
destroy $w
toplevel $w
wm title $w "Toolbar Demonstration"
wm iconname $w "toolbar"
positionWindow $w

if {[tk windowingsystem] ne "aqua"} {
    ttk::label $w.msg -wraplength 4i -text "This is a demonstration of how to do\
	    a toolbar that is styled correctly and which can be torn off. The\
	    buttons are configured to be \u201Ctoolbar style\u201D buttons by\
	    telling them that they are to use the Toolbutton style. At the left\
	    end of the toolbar is a simple marker that the cursor changes to a\
	    movement icon over; drag that away from the toolbar to tear off the\
	    whole toolbar into a separate toplevel widget. When the dragged-off\
	    toolbar is no longer needed, just close it like any normal toplevel\
	    and it will reattach to the window it was torn off from."
} else {
ttk::label $w.msg -wraplength 4i -text "This is a demonstration of how to do\
	    a toolbar that is styled correctly. The buttons are configured to\
	    be \u201Ctoolbar style\u201D buttons by telling them that they are\
	    to use the Toolbutton style."
}

## Set up the toolbar hull
set t [frame $w.toolbar]		;# Must be a frame!
ttk::separator $w.sep
ttk::frame $t.tearoff -cursor fleur
if {[tk windowingsystem] ne "aqua"} {
    ttk::separator $t.tearoff.to -orient vertical
    ttk::separator $t.tearoff.to2 -orient vertical
    pack $t.tearoff.to -fill y -expand 1 -padx 2 -side left
    pack $t.tearoff.to2 -fill y -expand 1 -side left
}
ttk::frame $t.contents
grid $t.tearoff $t.contents -sticky nsew
grid columnconfigure $t $t.contents -weight 1
grid columnconfigure $t.contents 1000 -weight 1

if {[tk windowingsystem] ne "aqua"} {
    ## Bindings so that the toolbar can be torn off and reattached
    bind $t.tearoff     <B1-Motion> [list tearoff $t %X %Y]
    bind $t.tearoff.to  <B1-Motion> [list tearoff $t %X %Y]
    bind $t.tearoff.to2 <B1-Motion> [list tearoff $t %X %Y]
    proc tearoff {w x y} {
	if {[string match $w* [winfo containing $x $y]]} {
	    return
	}
	grid remove_creature $w
	grid remove_creature $w.tearoff
	wm manage $w
	wm protocol $w WM_DELETE_WINDOW [list untearoff $w]
    }
    proc untearoff {w} {
	wm forget $w
	grid $w.tearoff
	grid $w
    }
}

## Toolbar contents
ttk::button $t.button -text "Button" -style Toolbutton -command [list \
	$w.txt insert end "Button Pressed\n"]
ttk::checkbutton $t.check -text "Check" -variable check -style Toolbutton \
	-command [concat [list $w.txt insert end] {"check is $check\n"}]
ttk::menubutton $t.menu -text "Menu" -menu $t.menu.m
ttk::combobox $t.combo -value [lsort [font families]] -state readonly
menu $t.menu.m
$t.menu.m add command -label "Just" -command [list $w.txt insert end Just\n]
$t.menu.m add command -label "An" -command [list $w.txt insert end An\n]
$t.menu.m add command -label "Example" \
	-command [list $w.txt insert end Example\n]
bind $t.combo <<ComboboxSelected>> [list changeFont $w.txt $t.combo]
proc changeFont {txt combo} {
    $txt configure -font [list [$combo get] 10]
}

## Some content for the rest of the toplevel
text $w.txt -width 40 -height 10
interp alias {} doInsert {} $w.txt insert end	;# Make bindings easy to write

## Arrange contents
grid $t.button $t.check $t.menu $t.combo -in $t.contents -padx 2 -sticky ns
grid $t -sticky ew
grid $w.sep -sticky ew
grid $w.msg -sticky ew
grid $w.txt -sticky nsew
grid rowconfigure $w $w.txt -weight 1
grid columnconfigure $w $w.txt -weight 1

## See Code / Dismiss buttons
set btns [addSeeDismiss $w.buttons $w]
grid $btns -sticky ew
