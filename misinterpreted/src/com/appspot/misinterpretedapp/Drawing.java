package com.appspot.misinterpretedapp;

import java.util.ArrayList;
import android.graphics.Bitmap;
import android.graphics.Canvas;
import android.graphics.Paint;

public class Drawing {
	
	// Data storage.
	private ArrayList<PenAction> actions;
	
	public Drawing() {
		actions = new ArrayList<PenAction>();
	}
	
	// For reading data. Use for (PenAction pa : someDrawing.getActionList())
	public ArrayList<PenAction> getActionList() {
		return actions;
	}
	
	// For writing data
	public void penDown(float x, float y) {
		actions.add(new PenAction(PenAction.PEN_DOWN, x, y));
	}
	public void penMove(float x, float y) {
		actions.add(new PenAction(PenAction.PEN_MOVE, x, y));
	}
	public void penUp(float x, float y) {
		actions.add(new PenAction(PenAction.PEN_UP, x, y));
	}
	public void changeColor(int color) {
		actions.add(new PenAction(color));
	}
	public void changeSize(float size) {
		actions.add(new PenAction(size));
	}
	
	public void addRawPenAction(PenAction pa) {
		actions.add(pa);
	}
	
	public boolean isBlank() { // is the drawing blank? i.e. does the list of actions contain nothing?
		return (actions.size() == 0);
	}
	
	public Bitmap toBitmap(float scale, int targetWidth, int targetHeight, float dp) {
		Bitmap bitmap = Bitmap.createBitmap(targetWidth, targetHeight, Bitmap.Config.ARGB_8888);
		Canvas canvas = new Canvas(bitmap);
		Paint defaultPaint = new Paint();
		float defaultSize = 3*dp;
		defaultPaint.setStrokeWidth(defaultSize*scale);
		defaultPaint.setColor(0xff000000);
		defaultPaint.setStrokeCap(Paint.Cap.ROUND);
		Paint drawingPaint = new Paint(defaultPaint);
		float prevX = 0; // these are measured in dp already and do NOT need prevX*dp
		float prevY = 0;
		for (PenAction pa : getActionList()) {
			switch (pa.action) {
			case PenAction.PEN_DOWN:
				canvas.drawPoint(pa.x*dp*scale, pa.y*dp*scale, drawingPaint);
				prevX = pa.x*dp*scale;
				prevY = pa.y*dp*scale;
				break;
			case PenAction.PEN_MOVE:
				canvas.drawLine(prevX, prevY, pa.x*dp*scale, pa.y*dp*scale, drawingPaint);
				prevX = pa.x*dp*scale;
				prevY = pa.y*dp*scale;
				break;
			case PenAction.PEN_UP:
				canvas.drawLine(prevX, prevY, pa.x*dp*scale, pa.y*dp*scale, drawingPaint);
				prevX = pa.x*dp*scale;
				prevY = pa.y*dp*scale;
				break;
			case PenAction.CHANGE_COLOR:
				drawingPaint.setColor(pa.color);
				break;
			case PenAction.CHANGE_SIZE:
				drawingPaint.setStrokeWidth(pa.size*scale);
				break;
			}
		}
		return bitmap;
	}
}
