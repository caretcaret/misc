package com.appspot.misinterpretedapp;

import android.app.Activity;
import android.content.res.Configuration;
import android.graphics.Bitmap;
import android.graphics.Typeface;
import android.os.Bundle;
import android.text.method.SingleLineTransformationMethod;
import android.util.DisplayMetrics;
import android.util.TypedValue;
import android.view.Gravity;
import android.view.Window;
import android.view.WindowManager;
import android.widget.FrameLayout;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.TextView;
import android.widget.LinearLayout.LayoutParams;

public class ViewActivity extends Activity {
	
	Game game;
	float screenHeight;
	float screenWidth;
	float dp;
	
	@Override
	public void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		
		// SETUP
		// Get device dimensions in dp.

		DisplayMetrics metrics = new DisplayMetrics();
		getWindowManager().getDefaultDisplay().getMetrics(metrics);
		dp = metrics.density;
		screenHeight = metrics.heightPixels;
		screenWidth = metrics.widthPixels;
		
		// Remove the title bar and set full screen mode.
		getWindow().setFlags(WindowManager.LayoutParams.FLAG_FULLSCREEN,
				WindowManager.LayoutParams.FLAG_FULLSCREEN);
		requestWindowFeature(Window.FEATURE_NO_TITLE);
		
		// Activate the view
		setContentView(R.layout.view);
		
		// Get the requested game filename and load the file.
		String filename = "";
		try {
		Bundle bundle = getIntent().getExtras();
		filename = bundle.getString("filename");
		game = Game.open(ViewActivity.this, filename);
		game.clean();
			for (int i = 0; i < game.numTextSlides+game.numDrawSlides; i++) {
				if (i % 2 == 0) // if the slide is a text slide
					addTextSlide(game.getTextSlide(i));
				else
					addDrawSlide(game.getDrawSlide(i));
			}
			
		} catch (Exception e) {
			addTextSlide("There was an error opening the file " + filename + ": " + e.toString());
		}
		
	}
	
	// TODO allow a menu option to move forward/back/delete
	
	public void addTextSlide(String text) {
		FrameLayout frameLayout = new FrameLayout(ViewActivity.this);
		frameLayout.setLayoutParams(new FrameLayout.LayoutParams(
				(int) screenWidth, (int) screenHeight));
		frameLayout.setBackgroundResource(R.drawable.linedpaper_repeat);
		TextView description = new TextView(ViewActivity.this);
		description.setText(text);
		FrameLayout.LayoutParams lp = new FrameLayout.LayoutParams(LayoutParams.FILL_PARENT,
				LayoutParams.WRAP_CONTENT);
		lp.gravity = Gravity.CENTER;
		description.setLayoutParams(lp);
		description.setGravity(Gravity.CENTER);
		// limit to a single line (returns are suppressed to spaces)
		description.setTransformationMethod(new SingleLineTransformationMethod());
		// set the font to something closer to handwritten
		description.setTypeface(Typeface.create(Typeface.SERIF, Typeface.ITALIC));
		description.setTextColor(0xff000000);
		description.setTextSize(TypedValue.COMPLEX_UNIT_SP, 20);
		frameLayout.addView(description);
		LinearLayout layoutGame = (LinearLayout) findViewById(R.id.layoutGame);
		layoutGame.addView(frameLayout);
	}
	
	public void addDrawSlide(Drawing drawing) {
		Bitmap drawingBitmap = drawing.toBitmap(1f, (int) screenWidth,
				(int) screenHeight, dp);
		ImageView imageView = new ImageView(ViewActivity.this);
		imageView.setImageBitmap(drawingBitmap);
		imageView.setBackgroundResource(R.drawable.canvas_repeat);
		LinearLayout layoutGame = (LinearLayout) findViewById(R.id.layoutGame);
		layoutGame.addView(imageView);
	}

	// Prevent orientation change from landscape.
	public void onConfigurationChanged(Configuration newConfig) {
		// ignore orientation/keyboard change
		super.onConfigurationChanged(newConfig);
	}
}
