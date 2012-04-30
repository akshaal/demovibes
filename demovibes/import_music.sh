#!/usr/bin/zsh

DIR=`dirname "$0"`

# Grabs all files in music/, tries to get artist and song name from filename, and imports.
# Expects music/Source - blahblahblah/Artist/Album/Songname.mp3

for x in music/*/*/*/*.mp3; do
    source=$(echo "$x" | cut -d '/' -f2 | cut -d- -f1)
    artist=$(echo "$x" | cut -d '/' -f3 | sed 's/_/ /g')
    album=$(echo "$x" | cut -d '/' -f4 | sed 's/_/ /g')
    title=$(echo "$x" | cut -d '/' -f5- | sed 's/....$//' | sed 's/_/ /g')

    # Remove track number from title
    if echo "$title" | grep -q -P '^[0-9]+\s*-'; then
        title=`echo "$title" | cut -d- -f2-`
    fi

    # Import
    echo "\n- File: $x\n    Artist: $artist\n    Album: $album\n    Title: $title\n    Source ID: $source"
    while true; do
        yn="y"
        case $yn in
            [Yy]* )
                args="$IMPORT_MUSIC_EXTRA_ARGS"

                # Copy
                if test ! -z "$MUSIC_DEST"; then
                    if test -e "$MUSIC_DEST/$x"; then
                        echo "ERROR: $MUSIC_DEST/$x already exist!"
                        exit 55
                    fi

                    cp --parents "$x" "$MUSIC_DEST/"
                fi

                # Check for tags info
                SDIR=`dirname "$x"`
                tags_file="$SDIR/tags"
                if test -e "$tags_file"; then
                    tags=`cat "$tags_file"`
                    echo "    Tags: $tags"
                    args="$args -T $tags"
                fi

                # Run
                if $DIR/pyImportMp3.py -f "$x" -s $source -a "$artist" -t "$title" "${(s: :)args}" -C; then
                    echo "Success"

                    if test ! -z "$MUSIC_DEST"; then
                        mv "$x" "$x-imported"
                    fi
                else
                    echo "Failure"

                    if test ! -z "$MUSIC_DEST"; then
                        rm "$MUSIC_DEST/$x"
                    fi
                fi

                break;;

            [Nn]* )
                echo "ERROR: Skipped."
                break;;

            * )
                echo "Please answer yes or no.";;
        esac
    done
done

#  LocalWords:  DEST
