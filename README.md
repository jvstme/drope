# Drope

Drope is a utility for receiving file uploads. The primary goal of the project is simplicity. It takes one command to start the service and one drag and drop to upload the files.

## Installation

Drope is distributed via pip. If you have Python 3.6+ and pip installed, run the following command:

```bash
pip install drope
```

## Usage

Once installed, drope can be run as follows:

```bash
drope
```

The command will start a lightweight web server and host a page for uploading files. By default, the page is only accessible on localhost. If you want to host it on all network interfaces, consider adding the `--host 0.0.0.0` option. See `drope --help` for the list of options.

## Contributing

If you would like to help develop the project, you are welcome to open an issue or a pull request on [GitHub](https://github.com/jvstme/drope).