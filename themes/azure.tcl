# Azure theme for ttk
# Inspiration from Microsoft's Fluent Design
# Author: Claude

namespace eval ttk::theme::azure {
    variable colors
    array set colors {
        -fg             "#ffffff"
        -bg             "#2d2d30"
        -disabledfg     "#a0a0a0"
        -disabledbg     "#3c3c40"
        -selectfg       "#ffffff"
        -selectbg       "#1976d2"
        -accent         "#0078d7"
        -accentdark     "#005b9f"
        -border         "#404045"
        -darkbg         "#252526"
        -lightbg        "#3e3e42"
    }

    proc LoadImages {imgdir} {
        variable I
        foreach file [glob -directory $imgdir *.png] {
            set img [file tail [file rootname $file]]
            set I($img) [image create photo -file $file]
        }
    }

    proc LoadImagesWithFallback {dir} {
        variable I
        if {[file exists $dir]} {
            LoadImages $dir
        } else {
            # Créer des images basiques par défaut
            set I(empty) [image create photo -width 1 -height 1]
        }
    }

    proc set_theme {} {
        variable colors
        variable I
        
        # Essayer de charger les images si disponibles
        set script_dir [file dirname [info script]]
        LoadImagesWithFallback [file join $script_dir "azure-img"]

        # Configure les couleurs et polices
        ttk::style configure . \
            -background $colors(-bg) \
            -foreground $colors(-fg) \
            -troughcolor $colors(-darkbg) \
            -focuscolor $colors(-accent) \
            -selectbackground $colors(-selectbg) \
            -selectforeground $colors(-selectfg)

        ttk::style map . \
            -background [list disabled $colors(-disabledbg) active $colors(-lightbg)] \
            -foreground [list disabled $colors(-disabledfg)] \
            -selectbackground [list !focus $colors(-accentdark)] \
            -selectforeground [list !focus white]

        # Configurer les widgets
        ttk::style configure TButton \
            -background $colors(-accent) \
            -foreground white \
            -padding {8 4}
            
        ttk::style map TButton \
            -background [list pressed $colors(-accentdark) active $colors(-accentdark) disabled $colors(-disabledbg)] \
            -foreground [list disabled $colors(-disabledfg)]

        ttk::style configure Accent.TButton \
            -background $colors(-accent) \
            -foreground white
            
        ttk::style map Accent.TButton \
            -background [list pressed $colors(-accentdark) active $colors(-accentdark) disabled $colors(-disabledbg)] \
            -foreground [list disabled $colors(-disabledfg)]

        ttk::style configure TCheckbutton \
            -background $colors(-bg) \
            -foreground $colors(-fg)
            
        ttk::style map TCheckbutton \
            -background [list disabled $colors(-disabledbg) active $colors(-lightbg)] \
            -foreground [list disabled $colors(-disabledfg)]

        ttk::style configure TRadiobutton \
            -background $colors(-bg) \
            -foreground $colors(-fg)
            
        ttk::style map TRadiobutton \
            -background [list disabled $colors(-disabledbg) active $colors(-lightbg)] \
            -foreground [list disabled $colors(-disabledfg)]

        ttk::style configure TEntry \
            -background $colors(-lightbg) \
            -foreground $colors(-fg) \
            -fieldbackground $colors(-lightbg) \
            -borderwidth 1 \
            -padding 4
            
        ttk::style map TEntry \
            -background [list disabled $colors(-disabledbg)] \
            -foreground [list disabled $colors(-disabledfg)] \
            -fieldbackground [list disabled $colors(-disabledbg)]

        ttk::style configure TCombobox \
            -background $colors(-lightbg) \
            -foreground $colors(-fg) \
            -fieldbackground $colors(-lightbg) \
            -arrowcolor $colors(-fg) \
            -padding 4
            
        ttk::style map TCombobox \
            -background [list disabled $colors(-disabledbg)] \
            -foreground [list disabled $colors(-disabledfg)] \
            -fieldbackground [list disabled $colors(-disabledbg)] \
            -arrowcolor [list disabled $colors(-disabledfg)]

        ttk::style configure TSpinbox \
            -background $colors(-lightbg) \
            -foreground $colors(-fg) \
            -fieldbackground $colors(-lightbg) \
            -arrowcolor $colors(-fg) \
            -padding 4
            
        ttk::style map TSpinbox \
            -background [list disabled $colors(-disabledbg)] \
            -foreground [list disabled $colors(-disabledfg)] \
            -fieldbackground [list disabled $colors(-disabledbg)] \
            -arrowcolor [list disabled $colors(-disabledfg)]

        ttk::style configure TNotebook \
            -background $colors(-darkbg) \
            -tabmargins {2 2 2 0}
            
        ttk::style configure TNotebook.Tab \
            -background $colors(-bg) \
            -foreground $colors(-fg) \
            -padding {10 4}
            
        ttk::style map TNotebook.Tab \
            -background [list selected $colors(-accent) active $colors(-lightbg) disabled $colors(-disabledbg)] \
            -foreground [list selected white disabled $colors(-disabledfg)]

        ttk::style configure TFrame \
            -background $colors(-bg)

        ttk::style configure TLabelframe \
            -background $colors(-bg) \
            -foreground $colors(-fg) \
            -borderwidth 1 \
            -relief groove
            
        ttk::style configure TLabelframe.Label \
            -background $colors(-bg) \
            -foreground $colors(-fg)

        ttk::style configure TLabel \
            -background $colors(-bg) \
            -foreground $colors(-fg)
            
        ttk::style map TLabel \
            -background [list disabled $colors(-bg)] \
            -foreground [list disabled $colors(-disabledfg)]

        ttk::style configure TProgressbar \
            -background $colors(-accent) \
            -troughcolor $colors(-darkbg)

        ttk::style configure TScale \
            -background $colors(-bg) \
            -troughcolor $colors(-darkbg) \
            -sliderrelief flat
            
        ttk::style map TScale \
            -background [list disabled $colors(-disabledbg)]
    }
}

proc set_theme {mode} {
    # Appliquer le thème Azure
    ttk::style theme create azure -parent default -settings {
        ttk::theme::azure::set_theme
    }
    ttk::style theme use azure
}