# pyFiller

## A tool that literally takes up space!

When you need to fill some filesystem space with patterned or random data, pyFiller fulfills your space-filling needs

Run `pyfiller --help` for usage details

## Common examples

- Fill the specified (existing) folder with random data, up to the limit of the filesystem:

        pyfiller --totalsize fill Y:\

- Create 200MiB files with random data, to a maximum of 750.5MiB, with colorful output:

        pyfiller --filesize 200MiB --totalsize 750.5MiB --colorful Y:\

- Create one 42MiB file with patterned data with colorful output:

        pyfiller --filesize 42MiB --totalsize 42MiB --pattern 0xA5FF00 --colorful Y:\
        pyfiller --filesize 42MiB --totalsize 42MiB --pattern "J=8675309 " --colorful Y:\

## Updating this package

Clone this repo

On a branch, make the required edits

Ensure you update the version number in `pyfiller/__config__.py`
(pre-release? use `rc` notation, e.g., `1.0.42rc99`)

### Build and install the distributable wheel

```bash
rm -rf pyfiller-* dist build *.egg-info
python setup.py bdist_wheel sdist
ls -al dist
pip uninstall -y pyfiller
pip install dist/*.whl
```

### Test the tools

The main tool is `pyfiller`

Run:

```bash
pyfiller --help
```

### Test the uploaded artifacts

```bash
pip uninstall -y pyfiller
pip install pyfiller
```
