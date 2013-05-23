package com.appspot.misinterpretedapp;

import android.content.Context;
import android.graphics.Canvas;
import android.graphics.Paint;
import android.graphics.Typeface;
import android.text.method.SingleLineTransformationMethod;
import android.util.TypedValue;
import android.view.Gravity;
import android.view.MotionEvent;
import android.view.View;
import android.view.View.OnTouchListener;
import android.view.inputmethod.EditorInfo;
import android.widget.EditText;
import android.widget.LinearLayout;

public class DrawView extends LinearLayout implements OnTouchListener {
	// Get screen dimensions in dp
	float screenWidth;
	float screenHeight;
	// Convert dp to px. e.g., 240 dp to px: use 240*dp.
	float dp;
	// Default radius of the drawing pen, in dp.
	//TODO float baseRadius;
	
	public Game game;
	public final static int ID_DESCRIPTION = 1337; // the id of the description EditText
	public final Paint defaultPaint;
	public Paint drawingPaint;
	public float defaultSize;
	public float drawingSize;
	// prevent more than one pointer from drawing.
	public int firstPointerID;
	
	public DrawView(Context context, int numPlayers, int mode, float screenHeight, float screenWidth, float dp) {
		super(context);
		setFocusable(true);
		setFocusableInTouchMode(true);
		setOnTouchListener(this);
		game = new Game(numPlayers, mode, screenWidth, screenHeight, dp);
		defaultPaint = new Paint();
		defaultPaint.setColor(0xff000000);
		defaultPaint.setStrokeCap(Paint.Cap.ROUND);
		drawingPaint = new Paint(defaultPaint);
		
		this.screenHeight = screenHeight;
		this.screenWidth = screenWidth;
		this.dp = dp;
		
		defaultSize = 3*dp;
		defaultPaint.setStrokeWidth(defaultSize);
		
		LinearLayout.LayoutParams lp = new LinearLayout.LayoutParams(LayoutParams.FILL_PARENT,
				LayoutParams.FILL_PARENT);
		this.setLayoutParams(lp);
	}
	
	@Override
	protected void onDraw(Canvas canvas) {
		if (game.getSlideType() == Game.SLIDE_DRAW) {
			drawingPaint = new Paint(defaultPaint);
			float prevX = 0; // these are measured in dp already and do NOT need prevX*dp
			float prevY = 0;
			for (PenAction pa : game.bufferDrawing.getActionList()) {
				switch (pa.action) {
				case PenAction.PEN_DOWN:
					canvas.drawPoint(pa.x*dp, pa.y*dp, drawingPaint);
					prevX = pa.x*dp;
					prevY = pa.y*dp;
					break;
				case PenAction.PEN_MOVE:
					canvas.drawLine(prevX, prevY, pa.x*dp, pa.y*dp, drawingPaint);
					prevX = pa.x*dp;
					prevY = pa.y*dp;
					break;
				case PenAction.PEN_UP:
					canvas.drawLine(prevX, prevY, pa.x*dp, pa.y*dp, drawingPaint);
					prevX = pa.x*dp;
					prevY = pa.y*dp;
					break;
				case PenAction.CHANGE_COLOR:
					drawingPaint.setColor(pa.color);
					break;
				case PenAction.CHANGE_SIZE:
					drawingPaint.setStrokeWidth(pa.size);
					break;
				}
			}
		}
		// update the screen
		invalidate();
	}
	
	@Override
	public boolean onTouch(View v, MotionEvent event) {
		if (game.getSlideType() == Game.SLIDE_DRAW) {
			switch (event.getAction()) {
			case MotionEvent.ACTION_DOWN:
				game.bufferDrawing.penDown(event.getX()/dp, event.getY()/dp); // get event in px, convert to dp
				firstPointerID = event.getPointerId(0);
				break;
			case MotionEvent.ACTION_MOVE:
				if (event.getPointerId(0) == firstPointerID) // prevent multitouch from ruining the drawing
					game.bufferDrawing.penMove(event.getX()/dp, event.getY()/dp);
				break;
			case MotionEvent.ACTION_UP:
				if (event.getPointerId(0) == firstPointerID)
					game.bufferDrawing.penUp(event.getX()/dp, event.getY()/dp);
				break;
			}
			return true;
		}
		return false;
	}
	
	public void setupSlideElements() {
		removeAllViews();
		if (game.getSlideType() == Game.SLIDE_TEXT) {
			EditText description = new EditText(getContext());
			if (game.getSlideIdx() == 0)
				description.setHint("Write something you would like to see drawn.");
			else {
				description.setHint("Describe what you see in the previous drawing.");
			}
			description.setId(ID_DESCRIPTION);
			// center the EditText
			LinearLayout.LayoutParams lp = new LinearLayout.LayoutParams(LayoutParams.FILL_PARENT,
					LayoutParams.WRAP_CONTENT);
			lp.gravity = Gravity.CENTER;
			description.setLayoutParams(lp);
			description.setGravity(Gravity.CENTER);
			// limit EditText to a single line (returns are suppressed to spaces)
			description.setTransformationMethod(new SingleLineTransformationMethod());
			// alternate background for EditText; prevents horrible border.
			description.setBackgroundResource(R.drawable.edittext_bg);
			// set the font to something closer to handwritten
			description.setTypeface(Typeface.create(Typeface.SERIF, Typeface.ITALIC));
			// prevent full screen IME for soft keyboards
			description.setImeOptions(EditorInfo.IME_FLAG_NO_EXTRACT_UI);
			description.setTextSize(TypedValue.COMPLEX_UNIT_SP, 20);
			addView(description);
		} else if (game.getSlideType() == Game.SLIDE_DRAW) {
			// do nothing
		}
	}
}
