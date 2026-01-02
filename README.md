# 📝 Todo App – Interactive CLI Application

A **beginner-friendly yet feature-rich command-line Todo application** built with Python.  
It offers a **beautiful Rich-based terminal UI**, **arrow key navigation**, and **comprehensive task management**, making it ideal for learning clean architecture and interactive CLI design.

---

## ✨ Features

### Core Functionality

- ✅ **Rich Interactive UI** – Elegant tables, colored output, panels, and icons
- ⌨️ **Arrow Key Navigation** – Navigate menus using Up/Down arrows and select with Enter
- 🚦 **Task Prioritization** – High, Medium, Low priority levels with clear color coding
- 📅 **Due Dates** – Natural language parsing (`tomorrow`, `next week`, `2024-12-31`)
- 🏷️ **Categories & Tags** – Organize todos using categories and multiple tags
- 🔍 **Search & Filtering** – Keyword search and advanced multi-criteria filtering
- 📊 **Statistics Dashboard** – Visual progress tracking and breakdowns
- ↩️ **Undo Last Action** – Single-level undo for add, delete, update, and complete
- ⚠️ **Enhanced UX** – Help menu, confirmations, and success/error alerts

---

## 🎯 Interactive Experience

- Guided prompts (no command memorization required)
- Keyboard shortcuts for fast navigation
- Color-coded display for priorities, due dates, and status
- Rich formatting using tables, panels, and progress bars
- Clear visual feedback with icons and messages

---

## 📋 Requirements

- **Python 3.11 or higher**
- Terminal with Unicode support  
  *(Windows Terminal, macOS Terminal, Linux terminal)*

---

## 🚀 Installation

### Quick Setup

```bash
# Clone the repository
git clone <repository-url>
cd todo-app

# Install dependencies
pip install -r requirements.txt

# Run the application
python -m src.menu
