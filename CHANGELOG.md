# Changelog

All notable changes to this project will be documented in this file.  
This project adheres to [Semantic Versioning](https://semver.org/).

---

## Semantic Versioning (SemVer)

The version number format is:

```

MAJOR.MINOR.PATCH

```

- **MAJOR** version when you make incompatible API changes  
- **MINOR** version when you add functionality in a backward-compatible manner  
- **PATCH** version when you make backward-compatible bug fixes  

### How to use it?

- Increase **MAJOR** version when you introduce changes that break backward compatibility (e.g., remove or modify public APIs).  
- Increase **MINOR** version when you add new features without breaking existing functionality.  
- Increase **PATCH** version when you fix bugs or make minor improvements without adding new features.  

---

## Example

```

1.0.0    # Initial release
1.1.0    # Added new features, backward-compatible
1.1.1    # Bug fixes and minor improvements
2.0.0    # Breaking changes, major rewrite, backward-incompatible

```

---

## Version History

## [1.0.3] – 24.06.2025
### Fistr functional exe file
- The executable *project_builder_cli.exe* has been built.
- First tests completed
- Better console logs

## [1.0.2] – 24.06.2025
### Created builder for .exe
- Created: ./src/app/build.py for building exe file
- Recreated structuro for project src, app, gui folders

## [1.0.1] – 24.06.2025
### Created tpl templates for automatic generated files
- Created: templates for `LICENSE`, `README`, `CHANGELOG`, `requirements` in cs/en and 'root' dir

## [1.0.0] – 24.06.2025
### Initial project
- Initial project skeleton created  
- Added: `README.md`, `LICENSE`, `requirements.txt`, and `docs/` folder
