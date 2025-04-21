# Modern theme for NightMod
# Clean, minimalist dark theme inspired by modern UI design trends

namespace eval ttk::theme::modern {
    variable colors
    # Palette de couleurs modernes et sombres
    array set colors {
        -fg             "#ffffff"
        -bg             "#1a1a1a"
        -disabledfg     "#9e9e9e"
        -disabledbg     "#383838"
        -selectfg       "#ffffff"
        -selectbg       "#4CAF50"
        -accent         "#4CAF50"       # Vert principal
        -accent2        "#2196F3"       # Bleu pour les variations
        -accentdark     "#388E3C"       # Vert foncé
        -border         "#424242"       # Gris foncé pour bordures subtiles
        -darkbg         "#121212"       # Très sombre pour arrière-plans
        -darkerbg       "#0a0a0a"       # Encore plus sombre
        -lightbg        "#2d2d2d"       # Plus léger pour contraste
        -cardcolor      "#252525"       # Couleur pour les composants "cartes"
        -divider        "#333333"       # Séparateurs
        -warning        "#ff9800"       # Orange pour alertes
        -error          "#f44336"       # Rouge pour erreurs
        -success        "#4caf50"       # Succès
        -info           "#2196f3"       # Info
    }
    
    # Initialiser les images
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
            
            # Créer quelques indicateurs de contrôle stylisés
            set I(radio-checked) [CreateRadioButton 12 1]
            set I(radio-unchecked) [CreateRadioButton 12 0]
            set I(check-checked) [CreateCheckButton 12 1]
            set I(check-unchecked) [CreateCheckButton 12 0]
        }
    }
    
    # Créer des indicateurs stylisés
    proc CreateRadioButton {size selected} {
        set img [image create photo -width $size -height $size]
        set center [expr {$size/2}]
        set radius [expr {$size/2 - 1}]
        set innerRadius [expr {$radius / 2}]
        
        # Créer un contexte de dessin
        package require Tk
        
        # Cercle extérieur (toujours présent)
        for {set y 0} {$y < $size} {incr y} {
            for {set x 0} {$x < $size} {incr x} {
                set dx [expr {$x - $center}]
                set dy [expr {$y - $center}]
                set distance [expr {hypot($dx, $dy)}]
                
                if {$distance <= $radius && $distance >= $radius-1} {
                    $img put "#4CAF50" -to $x $y [expr {$x+1}] [expr {$y+1}]
                }
            }
        }
        
        # Cercle intérieur (seulement si sélectionné)
        if {$selected} {
            for {set y 0} {$y < $size} {incr y} {
                for {set x 0} {$x < $size} {incr x} {
                    set dx [expr {$x - $center}]
                    set dy [expr {$y - $center}]
                    set distance [expr {hypot($dx, $dy)}]
                    
                    if {$distance <= $innerRadius} {
                        $img put "#4CAF50" -to $x $y [expr {$x+1}] [expr {$y+1}]
                    }
                }
            }
        }
        
        return $img
    }
    
    proc CreateCheckButton {size selected} {
        set img [image create photo -width $size -height $size]
        
        # Rectanglce extérieur
        if {$selected} {
            # Si sélectionné, couleur pleine
            for {set y 0} {$y < $size} {incr y} {
                for {set x 0} {$x < $size} {incr x} {
                    if {$x == 0 || $x == $size-1 || $y == 0 || $y == $size-1} {
                        # Bordure
                        $img put "#4CAF50" -to $x $y [expr {$x+1}] [expr {$y+1}]
                    } elseif {$x >= 2 && $y >= 2 && $x <= $size-3 && $y <= $size-3} {
                        # Intérieur
                        $img put "#4CAF50" -to $x $y [expr {$x+1}] [expr {$y+1}]
                    }
                }
            }
            
            # Dessin d'un checkmark
            if {$size >= 10} {
                # Points pour un checkmark
                set checkPoints [list \
                    [expr {$size/4}] [expr {$size/2}] \
                    [expr {$size/2.5}] [expr {$size/1.5}] \
                    [expr {$size/1.5}] [expr {$size/3}] \
                ]
                
                # Dessiner un checkmark blanc
                for {set i 0} {$i < [llength $checkPoints]-2} {incr i 2} {
                    set x1 [lindex $checkPoints $i]
                    set y1 [lindex $checkPoints [expr {$i+1}]]
                    set x2 [lindex $checkPoints [expr {$i+2}]]
                    set y2 [lindex $checkPoints [expr {$i+3}]]
                    
                    # Ligne simple
                    set dx [expr {$x2 - $x1}]
                    set dy [expr {$y2 - $y1}]
                    set steps [expr {max(abs($dx), abs($dy))}]
                    
                    for {set s 0} {$s <= $steps} {incr s} {
                        set x [expr {int($x1 + $s*$dx/$steps)}]
                        set y [expr {int($y1 + $s*$dy/$steps)}]
                        $img put "#FFFFFF" -to $x $y [expr {$x+1}] [expr {$y+1}]
                    }
                }
            }
        } else {
            # Si non sélectionné, juste un contour
            for {set y 0} {$y < $size} {incr y} {
                for {set x 0} {$x < $size} {incr x} {
                    if {$x == 0 || $x == $size-1 || $y == 0 || $y == $size-1} {
                        $img put "#888888" -to $x $y [expr {$x+1}] [expr {$y+1}]
                    }
                }
            }
        }
        
        return $img
    }
    
    # Configuration du thème
    proc set_theme {} {
        variable colors
        variable I
        
        # Charger des images pour les widgets
        set script_dir [file dirname [info script]]
        LoadImagesWithFallback [file join $script_dir "modern-img"]
        
        # Configuration générale
        ttk::style configure . \
            -background $colors(-bg) \
            -foreground $colors(-fg) \
            -troughcolor $colors(-darkbg) \
            -focuscolor $colors(-accent) \
            -selectbackground $colors(-selectbg) \
            -selectforeground $colors(-selectfg) \
            -borderwidth 0 \
            -insertwidth 1 \
            -insertcolor $colors(-fg)
            
        ttk::style map . \
            -background [list disabled $colors(-disabledbg) active $colors(-lightbg)] \
            -foreground [list disabled $colors(-disabledfg)] \
            -selectbackground [list !focus $colors(-accentdark)] \
            -selectforeground [list !focus $colors(-selectfg)]
            
        # Styles spécifiques pour les widgets
        
        # Frames
        ttk::style configure TFrame \
            -background $colors(-bg) \
            -borderwidth 0
            
        ttk::style configure Card.TFrame \
            -background $colors(-cardcolor) \
            -borderwidth 0 \
            -relief flat
            
        ttk::style configure Popup.TFrame \
            -background $colors(-darkbg) \
            -borderwidth 0
        
        # Labels
        ttk::style configure TLabel \
            -background $colors(-bg) \
            -foreground $colors(-fg) \
            -padding {3 3}
            
        ttk::style configure Title.TLabel \
            -font "TkDefaultFont 14 bold" \
            -foreground $colors(-fg)
            
        ttk::style configure PopupTitle.TLabel \
            -font "TkDefaultFont 18 bold" \
            -foreground $colors(-fg) \
            -background $colors(-darkbg)
            
        ttk::style configure Subtitle.TLabel \
            -font "TkDefaultFont 12 bold" \
            -foreground $colors(-fg)
            
        ttk::style configure Caption.TLabel \
            -font "TkDefaultFont 9" \
            -foreground $colors(-disabledfg)
            
        ttk::style configure Info.TLabel \
            -foreground $colors(-disabledfg) \
            -font "TkDefaultFont 9"
        
        # Boutons principaux
        ttk::style configure TButton \
            -padding {8 6} \
            -background $colors(-lightbg) \
            -foreground $colors(-fg) \
            -borderwidth 0 \
            -relief flat
            
        ttk::style map TButton \
            -background [list pressed $colors(-darkbg) active $colors(-lightbg)] \
            -foreground [list disabled $colors(-disabledfg)]
        
        # Bouton d'accent (principal)
        ttk::style configure Primary.TButton \
            -background $colors(-accent) \
            -foreground white \
            -padding {10 8} \
            -relief flat
            
        ttk::style map Primary.TButton \
            -background [list pressed $colors(-accentdark) active $colors(-accentdark)] \
            -foreground [list disabled $colors(-disabledfg)]
        
        # Bouton secondaire
        ttk::style configure Secondary.TButton \
            -background $colors(-lightbg) \
            -foreground $colors(-fg) \
            -padding {10 8} \
            -relief flat
            
        ttk::style map Secondary.TButton \
            -background [list pressed $colors(-border) active $colors(-border)] \
            -foreground [list disabled $colors(-disabledfg)]
        
        # Bouton de l'écran de sommeil
        ttk::style configure Wake.TButton \
            -background $colors(-accent) \
            -foreground white \
            -padding {15 12} \
            -relief flat \
            -font "TkDefaultFont 13 bold"
            
        ttk::style map Wake.TButton \
            -background [list pressed $colors(-accentdark) active $colors(-accentdark)] \
            -foreground [list disabled $colors(-disabledfg)]
        
        # Bouton d'accent
        ttk::style configure Accent.TButton \
            -background $colors(-accent) \
            -foreground white \
            -padding {10 8} \
            -relief flat
            
        ttk::style map Accent.TButton \
            -background [list pressed $colors(-accentdark) active $colors(-accentdark)] \
            -foreground [list disabled $colors(-disabledfg)]
                
        # Checkbuttons et Radiobuttons
        ttk::style configure TCheckbutton \
            -background $colors(-bg) \
            -foreground $colors(-fg)
        
        ttk::style configure Card.TCheckbutton \
            -background $colors(-cardcolor) \
            -foreground $colors(-fg)
        
        ttk::style configure Switch.TCheckbutton \
            -background $colors(-bg) \
            -foreground $colors(-fg)
        
        ttk::style configure TRadiobutton \
            -background $colors(-bg) \
            -foreground $colors(-fg)
            
        ttk::style configure Card.TRadiobutton \
            -background $colors(-cardcolor) \
            -foreground $colors(-fg)
        
        # Entrées et combobox
        ttk::style configure TEntry \
            -background $colors(-darkbg) \
            -foreground $colors(-fg) \
            -fieldbackground $colors(-darkbg) \
            -borderwidth 0 \
            -padding {8 8}
        
        ttk::style configure TCombobox \
            -background $colors(-darkbg) \
            -foreground $colors(-fg) \
            -fieldbackground $colors(-darkbg) \
            -arrowcolor $colors(-accent) \
            -borderwidth 0 \
            -padding {8 8}
        
        ttk::style configure TSpinbox \
            -background $colors(-darkbg) \
            -foreground $colors(-fg) \
            -fieldbackground $colors(-darkbg) \
            -arrowcolor $colors(-accent) \
            -borderwidth 0 \
            -padding {8 8}
        
        # Scales et Progressbars
        ttk::style configure TScale \
            -background $colors(-bg) \
            -troughcolor $colors(-darkbg) \
            -borderwidth 0 \
            -sliderlength 20 \
            -sliderthickness 10 \
            -sliderrelief flat
            
        ttk::style map TScale \
            -background [list active $colors(-bg)] \
            -troughcolor [list active $colors(-darkbg)]
        
        ttk::style configure TProgressbar \
            -background $colors(-accent) \
            -troughcolor $colors(-darkbg) \
            -borderwidth 0
        
        # Séparateurs et LabelFrames
        ttk::style configure TSeparator \
            -background $colors(-divider)
        
        ttk::style configure TLabelframe \
            -background $colors(-bg) \
            -foreground $colors(-fg) \
            -borderwidth 1 \
            -relief flat
            
        ttk::style configure TLabelframe.Label \
            -background $colors(-bg) \
            -foreground $colors(-fg) \
            -padding {5 2}
    }
}

proc set_theme {mode} {
    # Création et application du thème
    ttk::style theme create modern -parent default -settings {
        ttk::theme::modern::set_theme
    }
    ttk::style theme use modern
}