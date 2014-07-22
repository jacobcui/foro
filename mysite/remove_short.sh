#!/bin/bash
find . -type f -size -2|grep '.jpg'|xargs -I{} rm {}
