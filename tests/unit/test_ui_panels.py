"""
Unit tests for UI panels

Tests panel rendering functions:
- render_alert_panel() - success/error/warning/info alerts
- render_statistics_panel() - statistics dashboard (already tested in test_statistics.py)
"""

import pytest
from rich.panel import Panel
from src.ui.panels import render_alert_panel


class TestRenderAlertPanel:
    """Test render_alert_panel() function"""

    def test_render_alert_panel_success(self):
        """Should render success alert with green border"""
        panel = render_alert_panel("Operation successful", alert_type="success")

        assert isinstance(panel, Panel)
        assert "Operation successful" in panel.renderable
        assert panel.border_style == "green"
        assert "✓" in panel.title or "✓" in str(panel.renderable)

    def test_render_alert_panel_error(self):
        """Should render error alert with red border"""
        panel = render_alert_panel("Operation failed", alert_type="error")

        assert isinstance(panel, Panel)
        assert "Operation failed" in panel.renderable
        assert panel.border_style == "red"
        assert "✗" in panel.title or "✗" in str(panel.renderable)

    def test_render_alert_panel_warning(self):
        """Should render warning alert with yellow border"""
        panel = render_alert_panel("Warning message", alert_type="warning")

        assert isinstance(panel, Panel)
        assert "Warning message" in panel.renderable
        assert panel.border_style == "yellow"
        assert "⚠" in panel.title or "⚠" in str(panel.renderable)

    def test_render_alert_panel_info(self):
        """Should render info alert with blue border"""
        panel = render_alert_panel("Information", alert_type="info")

        assert isinstance(panel, Panel)
        assert "Information" in panel.renderable
        assert panel.border_style == "blue"
        assert "ℹ" in panel.title or "ℹ" in str(panel.renderable)

    def test_render_alert_panel_default_is_info(self):
        """Should default to info type if not specified"""
        panel = render_alert_panel("Default message")

        assert isinstance(panel, Panel)
        assert panel.border_style == "blue"

    def test_render_alert_panel_invalid_type_raises_error(self):
        """Should raise ValueError for invalid alert type"""
        with pytest.raises(ValueError) as exc_info:
            render_alert_panel("Message", alert_type="invalid")

        assert "alert_type must be one of" in str(exc_info.value)

    def test_render_alert_panel_with_long_message(self):
        """Should handle long messages"""
        long_message = "A" * 200
        panel = render_alert_panel(long_message, alert_type="success")

        assert isinstance(panel, Panel)
        assert long_message in panel.renderable

    def test_render_alert_panel_with_newlines(self):
        """Should handle multi-line messages"""
        multiline = "Line 1\nLine 2\nLine 3"
        panel = render_alert_panel(multiline, alert_type="info")

        assert isinstance(panel, Panel)
        assert "Line 1" in panel.renderable
        assert "Line 2" in panel.renderable
        assert "Line 3" in panel.renderable
