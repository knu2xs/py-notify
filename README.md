# Esri Commercial Team Notifications

This package enables sending email and text messages from a Python script, but it is mandatory to create a `notify/resources` directory containing a file named `credentials.json` before use. Once configured, it can be used to send email as part of a geoprocessing workflow, typically for either emergency notification, or simply to know when a long running workflow is complete.

## Configuration

Inside the `notify` directory, create another directory called 