# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is a Chinese traditional astrology (八字/Bazi) calculation and analysis system written in Python. The system includes both command-line tools for traditional calculations and a web-based interactive game deployed on Netlify.

## Project Structure

The codebase has dual architecture:
1. **Core Python calculators** - Traditional command-line astrology tools
2. **Web application** - Interactive Bazi relationship game with frontend/backend

### Core Modules (Traditional Calculations)
- **bazi.py** - Primary eight-character (八字) chart calculator and analysis tool
- **luohou.py** - Calculates Rahu (罗喉) times for feng shui compass usage  
- **shengxiao.py** - Chinese zodiac compatibility analysis
- **common.py** - Shared utility functions across modules
- **datas.py** - Core astrological data (star constellations, calendar mappings)
- **ganzhi.py** - Heavenly Stems (天干) and Earthly Branches (地支) system
- **sizi.py** - Four pillars analysis and interpretations
- **yue.py** - Month-related calculations

### Web Application Components
- **index.html** - Frontend game interface
- **app.py** - Local Flask development server 
- **netlify/functions/** - Serverless functions for production deployment
  - **bazi_utils.py** - Core game logic and chart generation
  - **new_game.py** - Game initialization endpoint
  - **check_relationship.py** - Relationship detection endpoint

## Installation and Dependencies

Install required Python dependencies:
```bash
pip install bidict lunar_python colorama flask flask-cors
```

## Development Commands

### Local Development
```bash
# Run local development server
python app.py

# Test individual calculators
python bazi.py 1977 8 11 19 -n
python shengxiao.py 虎
python luohou.py
```

### Testing
```bash
# Run specific test files (no unified test runner)
python test_game.py
python test_complete_flow.py
python simple_test.py
```

### Deployment
Deploys automatically to Netlify on git push to main branch. Configuration in `netlify.toml`.

## Core Data Architecture

### Traditional Chinese Calendar System
- **ganzhi60** - Complete 60-year cycle mapping (10 stems × 12 branches)
- **Bidirectional lookups** using `bidict` for efficient stem-branch conversions
- **Five-element scoring** (金木水火土) with seasonal adjustments
- **Calendar conversions** between Gregorian and traditional Chinese lunar calendar

### Relationship Detection System
The web game focuses on detecting relationships between chart elements:
- **天干五合** (Heavenly Stem combinations)
- **地支六合** (Earthly Branch six harmonies) 
- **地支三合局** (Earthly Branch triple harmonies)
- **地支三会方** (Earthly Branch directional meetings)
- **地支相冲** (Earthly Branch oppositions)
- **地支暗合** (Hidden combinations)

### Game Architecture
- **Chart generation** creates random valid Bazi charts
- **Relationship detection** finds all valid patterns in charts
- **Scoring system** rewards finding correct relationships
- **Progressive difficulty** with basic/advanced modes

## Usage Examples

### Traditional Calculator
```bash
python bazi.py 1977 8 11 19 -n
# -b: direct eight-character input
# -g: use Gregorian calendar 
# -r: leap month (lunar calendar only)
# -n: female chart (default is male)
```

### Web Game Development
```bash
# Start local server
python app.py
# Access at http://localhost:5000
```

## Cultural Context

This system implements traditional Chinese metaphysical calculations rooted in classical texts. The `books/` directory contains reference materials from traditional fortune-telling manuals, and `examples/` contains practical application cases for validation against historical charts.