package com.appspot.misinterpretedapp;

public class PenAction {
	public final static int PEN_DOWN = 0;
	public final static int PEN_MOVE = 1;
	public final static int PEN_UP = 2;
	public final static int CHANGE_COLOR = 3;
	public final static int CHANGE_SIZE = 4;
	public int action;
	public float x;
	public float y;
	public float size;
	public int color;
	public PenAction(int action, float x, float y) {
		this.action = action;
		this.x = x;
		this.y = y;
		this.size = -1;
		this.color = -1;
		// -1 for forward compatibility, in case size/color are specified for every PenAction.
	}
	public PenAction(float size) {
		this.action = CHANGE_SIZE;
		this.x = -1;
		this.y = -1;
		this.size = size;
		this.color = -1;
	}
	public PenAction(int color) {
		this.action = CHANGE_COLOR;
		this.x = -1;
		this.y = -1;
		this.size = -1;
		this.color = color;
	}
	public PenAction() { // empty uninitialized PenAction
		this.action = PEN_DOWN;
		this.x = -1;
		this.y = -1;
		this.size = -1;
		this.color = -1;
	}
}
