Agile Item Master
=================

This project is used for extracting our item master data from Agile using the Agile Java Library, and manipulate the data in such ways so it'll be possible to migrate it into Autodesk Fusion Lifecycle and NetSuite.

How to install
--------------

First, install the following dependencies:

* CPython 2.7 with pip and infi.projector installed
* Jython with pip installed

Once the dependencies are met, run the following commands:

* `projector devenv build --no-scripts`
* `python -m pip install -e .`
* `jython -m pip install -e .`

Last, before running this with Jython, you'll need to add the Agile JAR to your classpath.
To determine the location, run `export CLASSPATH="$(agile print classpath)"`


Dumping item master to CSV files
--------------------------------

In order to dump item master data, the following commands should be executed in the following order:

1. `agile dump items .`
2. `agile dump changes .`
3. `agile dump deviations .`
4. `agile group items .`
5. `agile explode bom .`
6. `agile reverse bom .`
7. `agile collapse bom .`
8. `agile merge ibox .`

Commands 1-3 must run over Jython since they pull the data from Agile, where there the rest should be executed with CPython for performance.

Command | Files | Notes
--------|-------|------
dump items | | CSV file per item type
dump changes | | CSV file per change type
dump deviations | | CSV file per deviation type
group items | Items and Revisions - Combined.csv | Groups all items and fields to one file table
explode bom | Exploded BOM.csv | Creates a recursive BOM file that can be imported to Autodesk
reverse bom | BOM (Parent Child).csv | Creates a simple structure for the parent-child relationships, used for migrating the data to NetSuite
collapse bom | Collapsed BOM (Parent Child).csv | Collapses upwards BOM elements that have only one child, making our the BOM easier to manage in NetSuite
merge ibox | IBOX (Merged).csv | Creates a command-separated lookup table we need for Workato in order to calculate SKUs until we migrate to Autodesk


Pushing item master to Workato
------------------------------

There are two ways to push the item master data to NetSuite via Workato:

* Process an ECO by first pushing all items and then their BOMs
* Pushing data from the dumped CSV files

The command-line syntax is:

    workato process change <number> [(--bom-only) | (--without-bom)] | [--dry-run | --retry-requests]
    workato process items <working-directory> [--part-type=TYPE | --item-number=NUMBER [--item-revision=REV]] [(--bom-only) | (--without-bom)] [--dry-run | --retry-requests]

The first needs to be executed with Jython as it accesses Agile, the second should be executed with CPython as it is much faster.
