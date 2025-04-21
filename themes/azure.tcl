# Azure theme for ttk
# Version améliorée pour NightMod
# Inspiration de Microsoft Fluent Design

namespace eval ttk::theme::azure {
    variable colors
    array set colors {
        -fg             "#f0f0f0"
        -bg             "#252526"
        -disabledfg     "#a0a0a0"
        -disabledbg     "#3c3c40"
        -selectfg       "#ffffff"
        -selectbg       "#1976d2"
        -accent         "#4CAF50"       # Vert plus apaisant
        -accent2        "#2196F3"       # Bleu pour variation
        -accentdark     "#3C9E3C"       # Vert foncé
        -border         "#404045"
        -darkbg         "#1e1e1e"       # Plus foncé pour meilleur contraste
        -darkerbg       "#171717"       # Encore plus foncé pour certains éléments
        -lightbg        "#303032"       # Plus léger mais toujours sombre
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
        
        # Thème adapté pour NightMod avec un design minimaliste et moderne
        # Idéal pour une utilisation nocturne confortable
        
        # Essayer de charger les images si disponibles
        set script_dir [file dirname [info script]]
        LoadImagesWithFallback [file join $script_dir "azure-img"]

        # Configure les couleurs et polices globales
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

        # Styles des boutons améliorés
        ttk::style configure TButton \
            -background $colors(-lightbg) \
            -foreground $colors(-fg) \
            -padding {10 6} \
            -relief flat
            
        ttk::style map TButton \
            -background [list pressed $colors(-darkbg) active $colors(-lightbg) disabled $colors(-disabledbg)] \
            -foreground [list disabled $colors(-disabledfg)]

        # Bouton d'accent - Important mais pas agressif
        ttk::style configure Accent.TButton \
            -background $colors(-accent) \
            -foreground white \
            -padding {10 6} \
            -relief flat
            
        ttk::style map Accent.TButton \
            -background [list pressed $colors(-accentdark) active $colors(-accentdark) disabled $colors(-disabledbg)] \
            -foreground [list disabled $colors(-disabledfg)]
        
        # Bouton pour la fenêtre de sommeil - Plus grand et visible
        ttk::style configure Sleep.TButton \
            -background $colors(-accent) \
            -foreground white \
            -padding {12 8} \
            -relief flat
            
        ttk::style map Sleep.TButton \
            -background [list pressed $colors(-accentdark) active $colors(-accentdark) disabled $colors(-disabledbg)] \
            -foreground [list disabled $colors(-disabledfg)]

        # Widgets de sélection avec style arrondi
        ttk::style configure TCheckbutton \
            -background $colors(-bg) \
            -foreground $colors(-fg) \
            -padding {2 2}
            
        ttk::style map TCheckbutton \
            -background [list disabled $colors(-disabledbg) active $colors(-lightbg)] \
            -foreground [list disabled $colors(-disabledfg)]

        ttk::style configure TRadiobutton \
            -background $colors(-bg) \
            -foreground $colors(-fg) \
            -padding {2 2}
            
        ttk::style map TRadiobutton \
            -background [list disabled $colors(-disabledbg) active $colors(-lightbg)] \
            -foreground [list disabled $colors(-disabledfg)]

        # Éléments d'entrée avec un aspect plus moderne
        ttk::style configure TEntry \
            -background $colors(-darkbg) \
            -foreground $colors(-fg) \
            -fieldbackground $colors(-darkbg) \
            -borderwidth 1 \
            -relief flat \
            -padding 6
            
        ttk::style map TEntry \
            -background [list disabled $colors(-disabledbg) focus $colors(-lightbg)] \
            -foreground [list disabled $colors(-disabledfg)] \
            -fieldbackground [list disabled $colors(-disabledbg) focus $colors(-darkbg)]

        ttk::style configure TCombobox \
            -background $colors(-darkbg) \
            -foreground $colors(-fg) \
            -fieldbackground $colors(-darkbg) \
            -arrowcolor $colors(-accent) \
            -relief flat \
            -padding 6
            
        ttk::style map TCombobox \
            -background [list disabled $colors(-disabledbg) focus $colors(-lightbg)] \
            -foreground [list disabled $colors(-disabledfg)] \
            -fieldbackground [list disabled $colors(-disabledbg) focus $colors(-darkbg)] \
            -arrowcolor [list disabled $colors(-disabledfg)]

        ttk::style configure TSpinbox \
            -background $colors(-darkbg) \
            -foreground $colors(-fg) \
            -fieldbackground $colors(-darkbg) \
            -arrowcolor $colors(-accent) \
            -relief flat \
            -padding 6
            
        ttk::style map TSpinbox \
            -background [list disabled $colors(-disabledbg) focus $colors(-lightbg)] \
            -foreground [list disabled $colors(-disabledfg)] \
            -fieldbackground [list disabled $colors(-disabledbg) focus $colors(-darkbg)] \
            -arrowcolor [list disabled $colors(-disabledfg)]

        # Conteneurs avec aspect plus moderne
        ttk::style configure TNotebook \
            -background $colors(-darkerbg) \
            -borderwidth 0 \
            -tabmargins {2 2 2 0}
            
        ttk::style configure TNotebook.Tab \
            -background $colors(-bg) \
            -foreground $colors(-fg) \
            -padding {12 6} \
            -borderwidth 0
            
        ttk::style map TNotebook.Tab \
            -background [list selected $colors(-accent) active $colors(-lightbg) disabled $colors(-disabledbg)] \
            -foreground [list selected white disabled $colors(-disabledfg)]

        # Frames avec meilleur contraste
        ttk::style configure TFrame \
            -background $colors(-bg) \
            -borderwidth 0
        
        # Version plus sombre pour les popups
        ttk::style configure Dark.TFrame \
            -background $colors(-darkerbg) \
            -borderwidth 0
            
        ttk::style configure Dark.TLabel \
            -background $colors(-darkerbg) \
            -foreground $colors(-fg)

        ttk::style configure TLabelframe \
            -background $colors(-bg) \
            -foreground $colors(-fg) \
            -borderwidth 1 \
            -relief groove
            
        ttk::style configure TLabelframe.Label \
            -background $colors(-bg) \
            -foreground $colors(-fg) \
            -padding {5 2}

        # Labels avec variations stylistiques
        ttk::style configure TLabel \
            -background $colors(-bg) \
            -foreground $colors(-fg)
            
        ttk::style map TLabel \
            -background [list disabled $colors(-bg)] \
            -foreground [list disabled $colors(-disabledfg)]
            
        # Labels spéciaux pour le titre et le temps
        ttk::style configure Title.TLabel \
            -background $colors(-bg) \
            -foreground $colors(-fg) \
            -font "TkDefaultFont 14 bold"
            
        ttk::style configure Time.TLabel \
            -background $colors(-bg) \
            -foreground $colors(-accent) \
            -font "TkDefaultFont 24 bold"
            
        ttk::style configure Info.TLabel \
            -background $colors(-bg) \
            -foreground $colors(-disabledfg) \
            -font "TkDefaultFont 8"

        # Éléments pour visualiser les états
        ttk::style configure Progress.TFrame \
            -background $colors(-darkbg)
            
        ttk::style configure Progress.TLabel \
            -background $colors(-accent) \
            -foreground white

        # Barres de progression et glissières plus modernes
        ttk::style configure TProgressbar \
            -background $colors(-accent) \
            -troughcolor $colors(-darkbg) \
            -borderwidth 0

        ttk::style configure TScale \
            -background $colors(-bg) \
            -troughcolor $colors(-darkbg) \
            -borderwidth 0 \
            -sliderrelief flat \
            -sliderthickness 20
            
        ttk::style map TScale \
            -background [list disabled $colors(-disabledbg)]
            
        # Séparateurs subtils
        ttk::style configure TSeparator \
            -background $colors(-border)
        
        # Scrollbars modernisées
        ttk::style configure Vertical.TScrollbar \
            -background $colors(-bg) \
            -troughcolor $colors(-darkbg) \
            -borderwidth 0 \
            -arrowcolor $colors(-accent)
            
        ttk::style map Vertical.TScrollbar \
            -background [list active $colors(-lightbg) disabled $colors(-disabledbg)] \
            -arrowcolor [list disabled $colors(-disabledfg)]
            
        ttk::style configure Horizontal.TScrollbar \
            -background $colors(-bg) \
            -troughcolor $colors(-darkbg) \
            -borderwidth 0 \
            -arrowcolor $colors(-accent)
            
        ttk::style map Horizontal.TScrollbar \
            -background [list active $colors(-lightbg) disabled $colors(-disabledbg)] \
            -arrowcolor [list disabled $colors(-disabledfg)]
            
        # Menus déroulants et popups
        option add *Menu.background $colors(-darkbg)
        option add *Menu.foreground $colors(-fg)
        option add *Menu.activeBackground $colors(-accent)
        option add *Menu.activeForeground white
        option add *Menu.disabledForeground $colors(-disabledfg)
        option add *Menu.relief flat
        option add *Menu.borderWidth 1
        
        # Boîtes de dialogue
        option add *Dialog.msg.background $colors(-bg)
        option add *Dialog.msg.foreground $colors(-fg)
        
        # Tooltips améliorés
        option add *Tooltip.background $colors(-darkerbg)
        option add *Tooltip.foreground $colors(-fg)
        option add *Tooltip.borderWidth 0
    }
}

# La fonction principale est appelée une seule fois depuis l'extérieur
proc set_theme {mode} {
    # Appliquer le thème Azure
    ttk::style theme create azure -parent default -settings {
        ttk::theme::azure::set_theme
    }
    ttk::style theme use azure
}