# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is a Chinese traditional astrology (八字/Bazi) calculation and analysis system written in Python. The codebase consists of several specialized modules for different aspects of Chinese astrology and divination.

## Installation and Dependencies

Install required dependencies before running any scripts:
```bash
pip install bidict lunar_python colorama
```

## Core Modules and Architecture

### Main Applications
- **bazi.py** - Primary eight-character (八字) chart calculator and analysis tool
- **luohou.py** - Calculates Rahu (罗喉) times for feng shui compass usage
- **shengxiao.py** - Chinese zodiac compatibility analysis

### Data and Utility Modules
- **common.py** - Common utility functions
- **convert.py** - Conversion utilities 
- **datas.py** - Core astrological data definitions (star constellations, calendar data)
- **ganzhi.py** - Heavenly Stems (天干) and Earthly Branches (地支) system implementation
- **sizi.py** - Four pillars analysis and interpretations
- **yue.py** - Month-related calculations

## Usage Examples

### Bazi Chart Analysis
```bash
python bazi.py 1977 8 11 19 -n
# Arguments: year month day time
# -b: direct eight-character input
# -g: use Gregorian calendar 
# -r: leap month (lunar calendar only)
# -n: female chart (default is male)
```

### Zodiac Compatibility
```bash
python shengxiao.py 虎
# Shows compatible and incompatible zodiac signs
```

### Rahu Time Calculation
```bash
python luohou.py
# Displays dates with inauspicious times for compass use
```

## Code Structure

### Data Architecture
- Chinese calendar and astronomical data stored in structured dictionaries
- Bidirectional mappings using `bidict` for efficient lookups
- Five-element (五行) scoring and analysis system
- Traditional fortune-telling interpretations integrated

### Key Data Structures
- **Gan/Zhi arrays** - 10 Heavenly Stems and 12 Earthly Branches
- **ganzhi60** - 60-year cycle mapping 
- **zhi5** - Five-element associations for earthly branches
- **wuhangs** - Five-element categorizations
- **temps** - Temperature/seasonal attributes

### Calculation Flow
1. Convert input dates to traditional Chinese calendar
2. Calculate four pillars (年月日时) using stem-branch system
3. Analyze element balance and seasonal considerations
4. Apply traditional interpretation rules
5. Generate detailed analysis with life period predictions

## Testing and Development

No formal test suite is included. Test calculations by comparing outputs with known reference charts or traditional almanacs.

## Cultural Context

This system implements traditional Chinese metaphysical calculations. The codebase contains classical Chinese fortune-telling texts and interpretations in the `books/` and `examples/` directories for reference and validation.