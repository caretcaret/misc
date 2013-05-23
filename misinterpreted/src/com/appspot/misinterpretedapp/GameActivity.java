package com.appspot.misinterpretedapp;

import android.app.Activity;
import android.app.AlertDialog;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.res.Configuration;
import android.graphics.Bitmap;
import android.os.Bundle;
import android.util.DisplayMetrics;
import android.view.Menu;
import android.view.MenuInflater;
import android.view.MenuItem;
import android.view.Window;
import android.view.WindowManager;
import android.view.inputmethod.InputMethodManager;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.Toast;

public class GameActivity extends Activity {	
	// Note: dv is drawView, but shortened for convenience. The game data is accessed
	//through dv at dv.game because dv also needs to access the game data.
	DrawView dv;
	
	@Override
	public void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		
		// SETUP
		// Get device dimensions in dp. Scale appropriately to vector:
		// store drawings as json data of lines/points. Pass to DrawView where this will be handled.

		DisplayMetrics metrics = new DisplayMetrics();
		getWindowManager().getDefaultDisplay().getMetrics(metrics);
		float dp = metrics.density;
		float screenHeight = metrics.heightPixels;
		float screenWidth = metrics.widthPixels;
		
		// Remove the title bar and set full screen mode.
		getWindow().setFlags(WindowManager.LayoutParams.FLAG_FULLSCREEN,
				WindowManager.LayoutParams.FLAG_FULLSCREEN);
		requestWindowFeature(Window.FEATURE_NO_TITLE);
		
		// Get the mode and number of text slides and draw slides from the previous Activity (SetupActivity).
		int numPlayers = 0;
		int mode = Game.MODE_OFFLINE;
		try {
			Bundle bundle = getIntent().getExtras();
			// create a new Game object to hold the data of the current game
			numPlayers = bundle.getInt("numPlayers");
			mode = bundle.getInt("mode");
		} catch (Exception e) {
			//try to show error for debugging
			Toast.makeText(GameActivity.this, e.toString(), Toast.LENGTH_LONG).show();
		}
		
		// set the content view to a new DrawView. This is never changed; at each slide change, the background
		// is changed instead and everything drawn/typed is reset. See displayNewSlide()
		dv = new DrawView(this, numPlayers, mode, screenHeight, screenWidth, dp);
		setContentView(dv);
		dv.requestFocus();
		
		// begin the first slide: text.
		displayNewSlide();
	}
	
	// Prevent orientation change from landscape.
	public void onConfigurationChanged(Configuration newConfig) {
		// ignore orientation/keyboard change
		super.onConfigurationChanged(newConfig);
	}
	
	
	// show menu options
	@Override
	public boolean onCreateOptionsMenu(Menu menu) {
		// initiate the menu. Set menu options for draw as invisible.
		MenuInflater inflater = getMenuInflater();
		inflater.inflate(R.menu.menu, menu);
		// no need to set irrelevant items as invisible; those are taken care
		// of in onPrepareOptionsMenu()
		return true;
	}
	
	@Override
	public boolean onPrepareOptionsMenu(Menu menu) {
		// update how far in the game the slide is
		menu.findItem(R.id.itemSlideNum).setTitle(Integer.toString(dv.game.getSlideIdx()+1) + "/" +
				Integer.toString(dv.game.numTextSlides + dv.game.numDrawSlides));
		// check for game slide type, show menu accordingly
		if (dv.game.getSlideType() == Game.SLIDE_TEXT) {
			menu.setGroupVisible(R.id.groupDraw, false);
			if (dv.game.getSlideIdx() != 0)
				menu.setGroupVisible(R.id.groupText, true);
			else
				menu.setGroupVisible(R.id.groupText, false);
			return true;
		} else if (dv.game.getSlideType() == Game.SLIDE_DRAW) {
			menu.setGroupVisible(R.id.groupDraw, true);
			menu.setGroupVisible(R.id.groupText, false);
			return true;
		}
		return false;
	}
	
	@Override
	public boolean onOptionsItemSelected(MenuItem item) {
		switch (item.getItemId()) {
		case R.id.itemPrevImage:
			prevContentsDialog();
			return true;
		case R.id.itemClear:
			dv.game.bufferDrawing = new Drawing();
			return true;
		case R.id.itemPrevText:
			prevContentsDialog();
			return true;
		case R.id.itemColorPicker:
			colorEraseDialog();
			return true;
		case R.id.itemSizePicker:
			sizeDialog();
			return true;
		case R.id.itemFinished:
			if (dv.game.getSlideType() == Game.SLIDE_TEXT) {
				EditText description = (EditText) findViewById(DrawView.ID_DESCRIPTION);
				dv.game.bufferDescription = (description.getText().toString());
				if (dv.game.bufferDescription.equals("")) { // check if any description text has been entered.
					Toast.makeText(GameActivity.this, "You must write a description.", Toast.LENGTH_SHORT).show();
				} else {
					// close the soft keyboard
					InputMethodManager imm = (InputMethodManager) getSystemService(Context.INPUT_METHOD_SERVICE);
					imm.hideSoftInputFromWindow(description.getWindowToken(), 0);
					displayNewSlide();
				}
			} else if (dv.game.getSlideType() == Game.SLIDE_DRAW) {
				if (dv.game.bufferDrawing.isBlank()) {// check if the user hasn't drawn anything
					Toast.makeText(GameActivity.this, "You must draw an image.", Toast.LENGTH_SHORT).show();
				}
				else {
					displayNewSlide();
				}
			}
			return true;
		default:
			return super.onOptionsItemSelected(item);
		}
	}
	
	@Override
	public void onBackPressed() {
		new AlertDialog.Builder(this)
			.setMessage("Are you sure you want to quit this game?")
			.setPositiveButton("Yes", new DialogInterface.OnClickListener() {
				public void onClick(DialogInterface dialog, int which) {
					if (dv.game.getSlideType() == Game.SLIDE_TEXT) { 
						EditText description = (EditText) findViewById(DrawView.ID_DESCRIPTION);
						dv.game.bufferDescription = (description.getText().toString());
						if (!dv.game.bufferDescription.equals(""))
							dv.game.store(dv.game.bufferDescription);
					} else if (dv.game.getSlideType() == Game.SLIDE_DRAW) {
						if (!dv.game.bufferDrawing.isBlank())
							dv.game.store(dv.game.bufferDrawing);
					}
					endGame();
				}
			})
			.setNegativeButton("No", new DialogInterface.OnClickListener() {
				public void onClick(DialogInterface dialog, int which) {
					// don't end the game
				}
			})
			.show();
	}
	public void prevContentsDialog() {
		AlertDialog.Builder builder = new AlertDialog.Builder(this);
		if (dv.game.getSlideType() == Game.SLIDE_TEXT) {
			Bitmap prevDrawingBitmap = dv.game.getPreviousDrawing().toBitmap(0.5f, (int) (dv.screenWidth/2), 
					(int) (dv.screenHeight/2), dv.dp);
			ImageView imageView = new ImageView(GameActivity.this);
			imageView.setImageBitmap(prevDrawingBitmap);
			imageView.setBackgroundResource(R.drawable.canvas_repeat);
			builder.setView(imageView);
			builder.setTitle("Write a description for this picture. Press back to continue...");
		} else if (dv.game.getSlideType() == Game.SLIDE_DRAW) {
			builder.setTitle("Draw an image of this. Press back to continue...");
			//TODO don't require back button
			builder.setMessage(dv.game.getPreviousDescription());
		}
		builder.show();
	}
	
	public void colorEraseDialog() {
		// TODO
		if (dv.game.getSlideType() == Game.SLIDE_DRAW) {
			AlertDialog.Builder builder = new AlertDialog.Builder(this);
			builder.setTitle("Select a color or the eraser tool.");
			builder.setMessage("to be implemented");
			builder.show();
		}
	}
	
	public void sizeDialog() {
		// TODO
		if (dv.game.getSlideType() == Game.SLIDE_DRAW) {
			AlertDialog.Builder builder = new AlertDialog.Builder(this);
			builder.setTitle("Select a size.");
			builder.setMessage("to be implemented");
			builder.show();
		}
	}

	public void displayNewSlide() {
		dv.game.startNextSlide();
		if (dv.game.getSlideType() == Game.SLIDE_END) {
			endGame();
		} else if (dv.game.getSlideType() == Game.SLIDE_TEXT) {
			// set the background to the tiled lined paper background
			dv.setBackgroundResource(R.drawable.linedpaper_repeat);
			dv.setupSlideElements();
			if (dv.game.getSlideIdx() != 0) prevContentsDialog();
		} else if (dv.game.getSlideType() == Game.SLIDE_DRAW) {
			// set the background to the tiled canvas background
			dv.setBackgroundResource(R.drawable.canvas_repeat);
			dv.setupSlideElements();
			if (dv.game.getSlideIdx() != 0) prevContentsDialog();
		}
		// do not put anything after the conditional, or else the end of the game
		// will run extra code
	}
	
	public void endGame() {
		// handle missing descriptions/drawings
		dv.game.clean();
		if (dv.game.numTextSlides > 0) {
			Intent intent;
			intent = new Intent(this, ViewActivity.class);
			// add filename to bundle
			String filename = dv.game.save(GameActivity.this, null, Game.MODE_OFFLINE);
			intent.putExtra("filename", filename);
			startActivity(intent);
			finish();
		} else { // if the game has not been started yet (no text slides after clean())
			finish();
		}
	}
}