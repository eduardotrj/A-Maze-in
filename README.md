 *This project has been created as part of 42 curriculum by ecakiray, etrujill.*


---
Duties for Docs (Index will come from this):
- [ ] Docs with:
    - [ ] Init and use maze instructions.
    - [ ] Pass custom parameters.
    - [ ] Access to generate structure and least 1 solution.
    - [ ] Structure, format of config file.
    - [ ] Maze generator algorith
    - [ ] WHy got this algorithm
    - [ ] What and how use reusable code
    - [ ] Roles for each team member
    - [ ] Anticipate planning and project development.
    - [ ] What works well and what can be improved
    - [ ] Specific tools used.
---


# A-Maze-ing

Visuals ...

Overview ...


---
## Table of Contents

- [Description](#description)
- [Description](#description)
- [Description](#description)

---
## Description
...

## Quick Start

### Prerequisites & Setup

### Installation

### Usage


## Structure

### Diagram

### Environment Variables

### External Tools

### Maze Generator Algorithms

### Reusability Code

### Testing


## Design & Development

### Planing

### Python Version

For Python version, we decided to use a more modern version over 3.10. After check all the different versions and the different improvements. For this project, was not required to use multicore. We could not get an important advantage of the main features from the lastest versions, while we should require to work with different unknown external libraries. For these follow reasons, we decided keep the version 3.11 that we already knew and allowed us to have the followed advantages:

**Python 3.11**
- Stable and madure version
- Excellent support for scientific and graphics libraries (Most of the used for this project)
- Compatible with most packages like Numpy, SciPy, OpenCv, Pygame, etc...
- Widely used in many projects → More information and code examples

**New from 3.10**
- Faster CPython up to 10-60%.
- Fine-Grained Tracebacks: Error messages pipoint the exact failed character or expression.
- Exception Group: Allow to use `ExceptionGroup` and `except*` to handle multiple exceptions simultaneously (wonderful to use).
- TOML Support: Support to read TOML configuration files → Perfect to use with Poetry 😬👉👉.

**Disadvantages**
- Not included newest language features.
- Not proper multithread support.
- Lower performance than newest versions.

We required maximun compatibility with many packages and libreries, while we don't expect to use complex algorithms and high volume of data than could require a better performance. Almost not experience to troubleshooting compatibility issues → Run for lastest versions. 

### Virtual Environment

Working in a big Python project and how much easy would be to messy by using different packages and python versions. We decided to use a virtual environtment.

After search, specially along Reddit. We decided to keep working with `Poetry`, which already we used in the project Python08, to handle the packages, to have more control in the project than regulrar `venv`.

### Split Duties

On this point, the first thing we did, is a short guide to work more properly and professional with GIT, in order to avoid future problems.

Then, we decided that by our skills we working mainly in one part of the project, but in some point, our roles will be exchanged, to have a more deep learning experience about this project.

**Edu:**
- Graphic generation of Mazes
- README file


**Eray:**
- Parsing
- Settings
- Generation Algorithms


### Features archieve

### Future Features and Improvements

---
## Resources

- [Python Versions](https://peps.python.org/pep-0000/)  - All information about the different Python versions.
- [Venv election](https://www.reddit.com/r/Python/comments/10bxkjp/what_are_people_using_to_organize_virtual/) Reddit post about which could be the best venv in Python (to be used in this project).
- [Git Convention](https://www.conventionalcommits.org/en/v1.0.0-beta.2/) Conventional commits information.
- [Gitignore](https://github.com/github/gitignore/blob/main/Python.gitignore) Main Resource of gitignore.
- [README Struture](https://www.freecodecamp.org/news/how-to-structure-your-readme-file/)