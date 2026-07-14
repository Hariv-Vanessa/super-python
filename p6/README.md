Python packages are a way to organize and structure code by grouping related modules into directories.

Creating and Accessing Packages
- Create a Directory: create a folder that will act as the package root.
- Add Modules: Inside the directory, add Python files (modules). Each module can contain related functions or classes.
- Add __init__.py: add an __init__.py file to the directory. This file tells Python that the directory should be treated as a package.
- Create Sub-packages (Optional): One can organize code further by creating subdirectories with their own __init__.py files.
- Import Modules: Modules or functions inside the package can be imported using dot notation, for example:
from mypackage.module1 import greet

## Define the __all__ variable
List of strings that indicate the names that should be imported when using the * operator.

## Define a variable called version
Holding the package version.

## Syntax
Users can import both packages and module.
Users can also import specific objects from a package or module.

### Absolute import
Absolute import involves a full path.
Example: from pkg1.subpkg2.subpkg3.subpkg4.module5 import fun6.

### Relative Import
Relative imports use dot(.) notation to specify a location.