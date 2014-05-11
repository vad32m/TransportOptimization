#!/usr/bin/env bash

function PkgIsInstalled
{
    pkg_list=$(dpkg-query --showformat '${Package} ${Status}\n' -W $1 | \
        grep 'ok installed$' | sed -n -e 's/ .* ok installed$//p')
    for pkg_name in $1
    do
        echo "$pkg_list" | grep -q "^$pkg_name\$"
        if [ $? -ne 1 ]; then
            return 0;
        fi
    done

    return 1
}
rm CGraph.png
python main.py
