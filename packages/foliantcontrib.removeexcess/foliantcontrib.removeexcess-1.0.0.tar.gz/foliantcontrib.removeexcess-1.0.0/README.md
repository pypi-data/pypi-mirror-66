# RemoveExcess

RemoveExcess is a preprocessor that removes unnecessary Markdown files that are not mentioned in the project’s `chapters`, from the temporary working directory.

## Installation

```bash
$ pip install foliantcontrib.removeexcess
```

## Config

To enable the preprocessor, add `removeexcess` to `preprocessors` section in the project config:

```yaml
preprocessors:
    - removeexcess
```

The preprocessor has no options.

## Usage

By default, all preprocessors are applied to each Markdown source file copied into the temporary working directory.

Often it’s needed not to include some files to the project’s `chapters`. But anyway, preprocessors will be applied to all source files, that will take extra time and may cause extra errors. Also, extra files may pass to backends that might be undesirable for security reasons.

When RemoveExcess preprocessor is enabled, unnecessary files will be deleted. Decide at your discretion to which place in the preprocessor queue to put it.
