# PureData
Pure data patches

## Setup

Unless otherwise noted these patches are built using the vanilla version of [Pure Data](http://puredata.info/)
I'm currently using Pd-0.53-2 on macOS

It's necessary to point Pd to the utils directory before running most of the patches in this repository (
    `pd->preferences->Path->New` and find the path on your disk on macOS)

## Directory Structure

### Generative
Contains patches for self playing music

### Utils
Contains reusable externals which encapsulate specific behaviour (e.g. level controls, MIDI controller mappings) which would be tiresome to repeat in every patch