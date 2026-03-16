## Running the program

After cloning the repositoy (main branch) run:

```bash
poetry install
poetry run python -m shapefile_processing
```

or

```bash
poetry run python src/shapefile_processing/__main__.py
```

### Unit tests

```bash
poetry run python -m unittest
```

or

```bash
poetry run python -m unittest discover -s tests -p "test_*.py" -v
```

### Running one specific unit test

```bash
poetry run python -m unittest tests.test_shapefile_manager
```

### Running mypy analysis (check type hints)

```bash
poetry run mypy
```

### Running ruff chack (see pyproject.toml for configuration)

- E - pycodestyle errors (style issues)
- F - Pyflakes (logic issues like unused imports, undefined names)
- I - import sorting rules (isort-style checks)
- D - docstring rules (pydocstyle)

```bash
poetry run ruff check src
```

#### Run specific ruff check e.g. missing docstrings (D1xx rules)

```bash
poetry run ruff check --select D1 src
```

All source code is in the `src/shapefile_processing` package. Unit tests are in the `tests` folder.

### Project structure
All code is in src/shapefile_processing package. Unit tests are separate in tests folder.

```text
src/
└─ shapefile_processing/
   ├─ __init__.py
   ├─ __main__.py
   ├─ shapefile_manager.py
   ├─ assets/
   │  └─ magnifying-glass.svg
   ├─ services/
   │  ├─ __init__.py
   │  ├─ data_quality_services.py
   │  └─ spatial_metrics_service.py
   └─ ui/
      ├─ __init__.py
      ├─ attribute_table_dialog.py
      ├─ help_dialog.py
      ├─ main_window.py
      ├─ map_renderer.py
      ├─ parameters_dialog.py
      └─ zoom_to_data_button.py
```

TODO:
- support for non-metric crs by reprojecting
- show polygon attributes by clicking on polygon
- option to display OSM tiles as background layer
- point layer for QC issues
- additional spatial attributes calculation
- detect mre QC issues
- easier installation and running (e.g. double click icon)