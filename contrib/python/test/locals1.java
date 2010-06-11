package com.allen_sauer.gwt.dnd.client;

import com.google.gwt.core.client.GWT;
import com.google.gwt.user.client.DOM;

import com.allen_sauer.gwt.dnd.client.util.DOMUtil;
import com.allen_sauer.gwt.dnd.client.util.Location;
import com.allen_sauer.gwt.dnd.client.util.WidgetLocation;

public class PickupDragController extends AbstractDragController {

  private void calcBoundaryOffset() {
    Location widgetLocation = new WidgetLocation(context.boundaryPanel, null);
    boundaryOffsetX = widgetLocation.getLeft()
        + DOMUtil.getBorderLeft(context.boundaryPanel.getElement());
    boundaryOffsetY = widgetLocation.getTop()
        + DOMUtil.getBorderTop(context.boundaryPanel.getElement());
  }

  private void checkGWTIssue1813(Widget child, AbsolutePanel parent) {
    if (!GWT.isScript()) {
      if (child.getElement().getOffsetParent() != parent.getElement()
          && !"HTML".equals(child.getElement().getOffsetParent().getNodeName())) {
        DOMUtil.reportFatalAndThrowRuntimeException("some text");
      }
    }
  }

  private DropController getIntersectDropController(int x, int y) {
    DropController dropController = dropControllerCollection.getIntersectDropController(x, y);
    return dropController != null ? dropController : boundaryDropController;
  }
}
