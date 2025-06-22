# Dashboard Feature Checklist

This checklist tracks all requested and discussed features for the Analog Daddy dashboard. Mark features as complete, in progress, or add notes as you develop.

## Roadmap

### Hello World

- [x] Dracula theme with CSS variables and assets directory
- [x] Modular Dash app structure (`app.py`, `layout.py`, `callbacks.py`, `assets/`, `__main__.py`)
- [x] Hello World Dash app
- [x] Color demo using Dracula variables
- [ ] Follow dracula theme for all the exisiting and any newly created elements.

### LUT Import

- [x] Import the LUT (drag and drop) or select from file picker.
- [x] Ability to import multiple LUT.
- [x] Toast notification for 2s showing import complete.
- [ ] Display LUT details (info, temperature, corner) in a neat table.
- [ ] Device selection drop downs.
- [ ] For multiple LUT's expand the display LUT details table.
- [ ] LUT details table inside a element which is hidden/revelead with a button click or keyboard shortcut.

### Variable Selection

- [ ] After device selection, should be able to select the variables in drop-downs.
- [ ] Independent variable drop down and parametric variable drop down to be mutually exclusive.
- [ ] ability to select design ratios as independent var and parametric vars.
- [ ] Logic to identify variable type (indepedent variable and dependent variable) using dimensions.
- [ ] dependent variable drop down with single variable mode and ratio mode.
- [ ] Ratio mode, reveals numerator and denominator drop downs (which should be mutulally exclusive)
- [ ] A text to show in ratio mode for numerator/denominator selections of dropdowns.
- [ ] Start, stop and step input boxes for selecting the indepenedent and parametric variables ranges.
- [ ] If length is not a independent variable or parametric variable, display a text box to enter length.
- [ ] populate the default values of independent and parametric variable ranges text boxes from LUT reading.
- [ ] ability to only accept valid values and/or SI prefixes in text boxes.
- [ ] All the elements in a neat-compact table, which is hideable using the same keybind as above or mouse click of button.
- [ ] All the above will might change based on the 'diff' mode when multiple LUT's are loaded.

### Plotting

- [ ] Create a place holder text element to show the correct variables are selected and the correct range is selected.
- [ ] Display the crafted `look_up` function.
- [ ] Plot the look_up function returned value. (Reference docs/notebooks/*.ipynb) for syntax.
- [ ] Appropriate plot labels and title generation with automatic legends, units etc.
- [ ] Ability for multiple tabs within a single page for different plots and different variable selection.
- [ ] Add import/export or save/load functionality for the plot states and tab states.
- [ ] Add documentation/help section in dashboard
- [ ] Dashboard tests in `tests/`

---

_Add or edit features as your preferences evolve. Use this checklist to guide incremental, reviewable development._
